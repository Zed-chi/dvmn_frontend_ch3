import requests

# import os
from bs4 import BeautifulSoup

# from pathvalidate import sanitize_filename
import urllib

"#content > .d_book > tbody > tr:first-child > td:first-child a"
SFICTION_URL = "http://tululu.org/l55/"


def get_first_link(html):
    soup = BeautifulSoup(html, "lxml")
    href = (
        soup.find("div", id="content")
        .find(class_="d_book")
        .find("a")
        .get("href")
    )
    link = urllib.parse.urljoin(SFICTION_URL, href)
    return link


def get_all_book_links_on_page(html):
    soup = BeautifulSoup(html, "lxml")
    hrefs = soup.select(
        "div#content table.d_book tr:first-child td:first-child a"
    )
    links = list(
        map(lambda a: urllib.parse.urljoin(SFICTION_URL, a.get("href")), hrefs)
    )
    return links


def get_url_content(url):
    res = requests.get(SFICTION_URL)
    res.raise_for_status()
    return res.text


def get_books_page(id):
    url = f"{SFICTION_URL}/{id}/"
    return get_url_content(url)


def get_links_from_10_pages():
    links = []
    for id in range(1, 11):
        html = get_books_page(id)
        links.extend(get_all_book_links_on_page(html))
    return links


if __name__ == "__main__":
    print(get_links_from_10_pages())