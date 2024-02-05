# Third-party imports
from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from decouple import config
from datetime import datetime, timedelta
import json
from PIL import Image
from io import BytesIO
import os
import io
import base64
from serpapi import GoogleSearch
from fastapi.middleware.cors import CORSMiddleware


# Internal imports
from utils import generate_text_from_gpt, trim_json, encode_image
from prompt import get_prompt
from scrapper import ebay_scrapper

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# global conversation history
conversation_history = {}


@app.get("/")
async def test():
    return {"API": "Working"}


@app.post("/uploadfile/")
async def incoming_messages(file: UploadFile = File(...)):
    try:
        # write in file
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            buffer.write(file.file.read())

        # Open and process the image
        with open(temp_file_path, "rb") as img_file:
            image = Image.open(img_file).convert("RGB")
            byte_arr = io.BytesIO()
            image.save(byte_arr, format="JPEG")
            byte_arr = byte_arr.getvalue()
            base64_image = base64.b64encode(byte_arr).decode("utf-8")

        message = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": get_prompt()},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ]

        gpt_response = await generate_text_from_gpt(message)

        # Delete the file from disk
        os.remove(temp_file_path)

        # Search on eBay using SERP API
        params = {
            "engine": "google",
            "q": gpt_response + " products site:ebay.com",
            # "q": "similar products on ebay for '" + gpt_response + "' ",
            "api_key": config("SERP_API_KEY"),  # Set your SERP API key
        }
        search = GoogleSearch(params)
        results = search.get_dict()

        # from serpapi import GoogleSearch

        # params = {
        # "engine": "google_lens",
        # "url": "https://i.ebayimg.com/images/g/pBcAAOSwEm9kexhR/s-l1200.webp",
        # "no_cache": True,
        # "api_key": ""
        # }

        # search = GoogleSearch(params)
        # results = search.get_dict()
        # visual_matches = results["visual_matches"]

        # return {"response": visual_matches}

        # Extract eBay URLs
        ebay_urls = [
            result["link"]
            for result in results["organic_results"]
            if "ebay.com" in result["link"]
        ]

        ebay_items = [item for item in ebay_urls if "itm" in item]

        response_data = []

        for item_url in ebay_items:
            heading, price, image_urls = ebay_scrapper(item_url)
            response_data.append(
                {"name": heading, "price": price, "image_urls": image_urls}
            )

        # return {"ebay_urls": ebay_items}
        return JSONResponse(content={"data": response_data})
    except Exception as e:
        print("Exception: ", e.with_traceback())
        return HTTPException(status_code=404, detail="Details Not Found")
