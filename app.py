import requests
import os
from utils import *


BASE_URL = "http://tululu.org"
BASE_BOOK_PAGE = "http://tululu.org/b"
BOOK_URL = "http://tululu.org/txt.php?id="


def download_10_books():
    for id in range(1, 11):
        download_txt_from_tululu_by_id(id)


def download_txt_from_tululu_by_id(id):
    book_url = f"{BOOK_URL}{id}"
    book_details_page = f"{BASE_BOOK_PAGE}{id}"
    txt = get_url_content(book_url)
    html = get_url_content(book_details_page, allow_redirects=True)
    info = get_book_details(html)
    if info and txt:
        filename = f"{id}.{info['title']}.txt"
        filepath = get_output_filename(filename)
        save_book(filepath, txt)
        print(f"{id} done")


def get_images_from_10_books():
    for id in range(1, 11):
        book_details_page = f"{BASE_BOOK_PAGE}{id}"
        html = get_url_content(book_details_page, allow_redirects=True)
        info = get_book_details(html)
        if info and info["img_url"] is not None:
            try:
                if "nopic" in info["img_url"]:
                    name = "nopic"
                else:
                    name = f"{id}"
                res = requests.get(info["img_url"])
                if res.status_code == 200:
                    print_book_details(info)
                    ext = info["img_url"].split(".")[-1]
                    save_image(f"{name}.{ext}", res.content)
            except Exception as e:
                print(e)


def download_100_books():
    books_path = os.path.join("./", "/books")
    images_path = os.path.join("./", "images")
    links = []
    description = {}
    for id in range(1, 2):
        html = get_sfiction_list_books_page(id)
        links.extend(get_all_book_links_on_page(html))
    for id, link in enumerate(links):
        html = get_url_content(link, allow_redirects=True)
        info = get_book_details(html)
        if "nopic" in info["img_url"]:
            name = "nopic"
        else:
            name = f"{id}"
        if requests.head(info["img_url"]).status_code == 200:
            ext = info["img_url"].split(".")[-1]
            filename = f"{name}.{ext}"
            info["img_src"] = os.path.join(images_path, filename)
            info["book_path"] = os.path.join(books_path, filename)            
            book_id = get_id_from_book_url(link)
            txt_link = f"{BOOK_URL}{book_id}"            
            download_image(from_=info["img_url"], to=info["img_src"])
            download_txt(from_=txt_link, to=info["book_path"])
            description.update(info)


if __name__ == "__main__":
    download_100_books()
