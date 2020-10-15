import urllib

from bs4 import BeautifulSoup

from utils import get_text_from_url

SFICTION_URL = "https://tululu.org/l55/"


def get_all_book_links_on_page(html):
    try:
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
    except Exception as e:
        print(e)


def get_sfiction_list_books_page(page_num):
    url = f"{SFICTION_URL}{page_num}/"
    return get_text_from_url(url)


def get_links_from_pages(startpage, endpage=None):
    links = []
    if endpage:
        for page_num in range(startpage, endpage):
            html = get_sfiction_list_books_page(page_num)
            if not html:
                continue
            links.extend(get_all_book_links_on_page(html))
    else:
        page_num = startpage
        while True:
            html = get_sfiction_list_books_page(page_num)
            if not html:
                break
            links.extend(get_all_book_links_on_page(html)) if html else None
            page_num += 1
    return links
