# Standard library import
import logging
import os
import io
import re
import time
import requests
import base64
import urllib.parse

# Third-party imports
from decouple import config
from datetime import datetime, timezone, timedelta


# firebase imports
from openai import OpenAI


open_api_key = config("OPENAI_API_KEY")
openaiClient = OpenAI(api_key=open_api_key)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def generate_text_from_gpt(content):
    try:
        response = openaiClient.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=content,
            temperature=0.1,
            max_tokens=1000,
        )

        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(response.choices[0].message.content)
        return response.choices[0].message.content
    except Exception as e:
        print("eE", e)
        logger.error(f"Error: {e}")


def trim_json(input2):
    trimed = ""
    flag = False

    for i in input2:
        # print(i)
        if i == "{":
            flag = True
        if flag:
            trimed += i

    trimed_2 = ""

    open_incr = 0

    for i in trimed:
        # print(i)
        if i == "{":
            open_incr += 1
        trimed_2 += i
        if i == "}":
            open_incr -= 1
        if open_incr == 0:
            break

    # Convert the trimmed dictionary back to a JSON string
    print("trimed_2", trimed_2)
    return trimed_2


# Function to encode the image
def encode_image(image):
    byte_arr = io.BytesIO()
    image.save(byte_arr, format="JPEG")
    byte_arr = byte_arr.getvalue()
    return base64.b64encode(byte_arr).decode("utf-8")


# fetch and store to file
def fetch_and_store_to_file(url, path):
    result = requests.get(url)
    with open(path, "w") as f:
        f.write(result.text)


def encode_for_url(query):
    return urllib.parse.quote_plus(query)
