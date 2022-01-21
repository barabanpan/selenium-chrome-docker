from time import sleep

from loguru import logger
from lxml.html import fromstring
import requests


def filter_smartphones_and_return_titles(first_n):
    url_with_filters = ("https://rozetka.com.ua/ua/mobile-phones/c80003/preset=smartfon;price=10000-20000;"
                        "producer=oneplus,samsung,xiaomi;protsessor-237281=qualsomm-snapdragon;sort=novelty;"
                        "23777=6-6-5,25316;38435=8-gb,12-gb;41404=16gb,256-gb1261112/")
    page = requests.get(url_with_filters)
    logger.debug("Opened smartphones")
    logger.debug("Sorted by brands")
    logger.debug("Sorted by RAM")
    logger.debug("Sorted by memory")
    logger.debug("Sorted by screen size")
    logger.debug("Sorted by processor")
    logger.debug("Sorted by price")
    logger.debug("Sorted by novelties")
    tree = fromstring(page.text)

    # take all phone ids
    id_elements = tree.xpath('//div[@class="goods-tile__inner"]')[:first_n]  # взяти data-goods-id
    ids = [e.get("data-goods-id") for e in id_elements]

    # open comparison page with found ids
    url_for_comparison = f"https://rozetka.com.ua/ua/comparison/c80003/ids={','.join(ids)}/"
    page = requests.get(url_for_comparison)
    tree = fromstring(page.text)
    logger.debug("Opened comparison page")

    # get smartphone names from comparison page
    name_elements = tree.xpath('//a[@class="product__heading"]')
    names = [e.text_content() for e in name_elements]
    for i, name in enumerate(names):
        print(f"{i + 1} - {name}")
