import requests
from bs4 import BeautifulSoup


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


# ebay_scrapper("https://www.ebay.com/itm/392130306467")
