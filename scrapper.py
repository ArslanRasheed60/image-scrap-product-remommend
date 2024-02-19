import requests
from bs4 import BeautifulSoup

from utils import fetch_and_store_to_file


def ebay_scrapper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    # print(soup.prettify())
    # fetching container
    container = soup.find("div", class_="vi-mast__grid")

    # heading of product
    heading = container.find("h1", class_="x-item-title__mainTitle")
    price = container.find("div", class_="x-price-primary").find("span").text
    divs = container.find_all(
        "div",
        class_=[
            "ux-image-carousel-item image-treatment active image",
            "ux-image-carousel-item image-treatment image",
        ],
    )
    # scraping urls
    image_urls = []
    for div in divs:
        img_tag = div.find("img")
        if img_tag and "data-zoom-src" in img_tag.attrs:
            image_urls.append(img_tag["data-zoom-src"])

    # print(heading.text)
    # print(image_urls)
    # print(price)
    return heading.text, price, image_urls


# scrapper for the sold auction item to get bid details
def ebay_auction_item_scrapper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    # print(soup.prettify())
    # fetching container
    container = soup.find("div", class_="vi-mast__grid")

    # heading of product
    heading = container.find("h1", class_="x-item-title__mainTitle")
    price = container.find("div", class_="x-price-primary").find("span").text
    number_of_bids = (
        container.find("div", class_="x-bid-info")
        .find("div", class_="x-bid-count")
        .find("a")
        .find("span")
        .text
    )
    divs = container.find_all(
        "div",
        class_=[
            "ux-image-carousel-item image-treatment active image",
            "ux-image-carousel-item image-treatment image",
        ],
    )
    # scraping urls
    image_urls = []
    count = 0
    for div in divs:
        img_tag = div.find("img")
        if img_tag and "data-zoom-src" in img_tag.attrs:
            image_urls.append(img_tag["data-zoom-src"])
            count += 1
        if count == 5:
            break

    # print(heading.text)
    # print(image_urls)
    # print(price)
    return heading.text, price, number_of_bids, image_urls


def ebay_sold_auction_items_list(item_str: str):
    try:
        ebay_url = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw={item_str}&_sacat=0&LH_Auction=1&LH_Sold=1&rt=nc&LH_PrefLoc=3"
        response = requests.get(ebay_url)
        soup = BeautifulSoup(response.content, "html.parser")

        # with open("./pages/p.html", "r") as file:
        #     html_content = file.read()
        # soup = BeautifulSoup(html_content, "html.parser")

        unordered_items = soup.find("ul", class_="srp-results srp-list clearfix")

        items_list = unordered_items.find_all(
            "li", class_="s-item s-item__pl-on-bottom"
        )

        # print("items_found: ", len(items_list))

        auction_item_details = []
        count = 0
        for item in items_list:
            # fetching image
            count += 1
            image_section_tag = item.find("div", class_="s-item__image-section")

            item_image_tag = image_section_tag.find("img")
            image_url = item_image_tag["src"]

            # anchor tag
            anchor_tag = image_section_tag.find("div").find("a")
            product_url = anchor_tag["href"]

            info_tag = item.find("div", class_="s-item__info clearfix")
            sold_span_text = (
                info_tag.find("div", class_="s-item__caption-section").find("span").text
            )

            # print("info_taginfo_taginfo_taginfo_taginfo_taginfo_tag", info_tag)

            heading_span_text = (
                info_tag.find("div", class_="s-item__title").find("span").text
            )

            details_tag = info_tag.find("div", class_="s-item__details clearfix")
            price_text = (
                details_tag.find("span", class_="s-item__price").find("span").text
            )
            number_of_bids_text = details_tag.find(
                "span", class_="s-item__bids s-item__bidCount"
            ).text

            auction_item_details.append(
                {
                    "name": heading_span_text,
                    "price": price_text,
                    "bids": number_of_bids_text,
                    "sold_text": sold_span_text,
                    "product_url": product_url,
                    "image_urls": [image_url],
                }
            )

            if count == 10:
                break

        return ebay_url, auction_item_details
    except Exception as e:
        print(e.__traceback__())
        return None


# testing parameters
# ebay_scrapper("https://www.ebay.com/itm/392130306467")

# auction_urls = ebay_sold_auction_items_list(
#     "Navy+puffer+jacket%2C+red+lining%2C+zipped+pockets."
# )
# heading, price, number_of_bids, image_urls = ebay_auction_item_scrapper(auction_urls[0])
# print(heading, price, number_of_bids, image_urls)
