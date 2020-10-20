import urllib

from bs4 import BeautifulSoup

from utils import get_text_from_url

SFICTION_URL = "https://tululu.org/l55/"


def get_all_book_links_on_page(html):
    soup = BeautifulSoup(html, "lxml")
    hrefs = soup.select(
        "div#content table.d_book tr:first-child td:first-child a"
    )
    links = list(
        map(
            lambda a: urllib.parse.urljoin(SFICTION_URL, a.get("href")),
            hrefs,
        )
    )
    return links


def get_sfiction_list_books_page(page_num):
    url = f"{SFICTION_URL}{page_num}/"
    return get_text_from_url(url)


def get_links_from_pages(startpage, endpage=None):
    links = []
    page_num = startpage
    while True:
        if endpage and page_num == endpage:
            return links
        html = get_sfiction_list_books_page(page_num)
        if not html:
            return links
        links.extend(get_all_book_links_on_page(html))
        page_num += 1
