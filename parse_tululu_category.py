from bs4 import BeautifulSoup
import urllib
from utils import get_text_from_url

SFICTION_URL = "http://tululu.org/l55/"


def get_all_book_links_on_page(html):
    soup = BeautifulSoup(html, "lxml")
    hrefs = soup.select(
        "div#content table.d_book tr:first-child td:first-child a"
    )
    links = list(
        map(lambda a: urllib.parse.urljoin(SFICTION_URL, a.get("href")), hrefs)
    )
    return links


def get_sfiction_list_books_page(page_num):
    url = f"{SFICTION_URL}{page_num}/"
    return get_text_from_url(url)


def get_links_from_pages(start, end=None):
    links = []
    if end:
        for page_num in range(start, end):
            html = get_sfiction_list_books_page(page_num)
            links.extend(get_all_book_links_on_page(html))
    else:
        page_num = start
        while True:
            html = get_sfiction_list_books_page(page_num)
            if not html:
                break
            links.extend(get_all_book_links_on_page(html))
            page_num += 1
    return links
