from dataclasses import dataclass
from decimal import Decimal
from typing import Callable

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

EBOOK_MAX = Decimal("9.99")
AVAILABLE = "Available"
SOLD_OUT = "Sold Out"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"


@dataclass()
class Scraper:
    name: str
    tag: str
    segments: set
    scraper: Callable[[], str]
    active: bool = True

    def __str__(self) -> str:
        return self.name


def scrape_scorp() -> str:
    url = "https://stoffercraft.com/products/spoon-scorp"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    form = soup.find("form", action="/cart/add")
    option = form.find("option")
    status = SOLD_OUT if "disabled" in option.attrs.keys() else AVAILABLE
    if status == SOLD_OUT:
        return ""

    price = form.find("span", id="productPrice").text
    return f"OG Scorp: {price}. {status}"


def scrape_paper() -> str:
    url = "https://stoffercraft.com/products/honing-paper"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    form = soup.find("form", action="/cart/add")
    options = form.find_all("option")
    option = options[0]
    status = SOLD_OUT if "disabled" in option.attrs.keys() else AVAILABLE
    if status == SOLD_OUT:
        return ""

    price = form.find("span", id="productPrice").text
    return f"Honing Paper: {price}. {status}"


def scrape_amazon_ebook() -> str:
    url = "https://www.amazon.co.uk/Last-Devil-Die-Thursday-Murder-ebook/dp/B0BCY25BMY/"
    with sync_playwright() as playwright:
        chromium = playwright.chromium
        browser = chromium.launch()
        page = browser.new_page()
        page.goto(url)
        data = page.content()

    soup = BeautifulSoup(data, "html.parser")

    a_string = soup.find(string=" Available instantly ")
    price = (
        a_string.find_parent()
        .parent.parent.parent.find("span", class_="a-color-price")
        .text.strip()
    )

    if Decimal(price.replace("£", "")) < EBOOK_MAX:
        return f"Richard Osmond ebook, The Last Devil to Die - Price Drop! {price} (down from £{EBOOK_MAX})"

    return ""
