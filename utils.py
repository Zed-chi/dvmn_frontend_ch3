import json
import os
import re
import urllib

from bs4 import BeautifulSoup

from pathvalidate import sanitize_filename

import requests


BASE_URL = "https://tululu.org"


def get_content_from_url(url, allow_redirects=False):
    response = requests.get(url, allow_redirects=allow_redirects)
    response.raise_for_status()
    return response.content    


def get_text_from_url(url, urlparams=None, allow_redirects=False):
    response = requests.get(
        url, allow_redirects=allow_redirects, params=urlparams
    )
    response.raise_for_status()
    return response.text    


def get_output_filename(filename):
    name = sanitize_filename(filename)
    path = os.path.normpath(name)
    return path


def get_id_from_book_url(link):
    result = re.search(r"b([0-9]+)", link)
    if not result:
        return
    return result.group(1)


def get_book_details(html):
    if not html:
        return None
    try:
        soup = BeautifulSoup(html, "lxml")
        header = soup.select("#content > h1")[0].text
        title, author = map(lambda text: text.strip(), header.split("::"))
        img = soup.select(".bookimage img")[0]
        if img:
            src = urllib.parse.urljoin(BASE_URL, img.get("src"))
        else:
            src = None
        comments = list(map(lambda tag: tag.text, soup.select(".texts span")))
        genres = list(
            map(lambda tag: tag.text, soup.select("#content > .d_book > a"))
        )

        return {
            "title": title,
            "author": author,
            "img_url": src,
            "comments": comments,
            "genres": genres,
        }
    except AttributeError as e:
        print(e)
    except TypeError as e:
        print(e)


def save_book(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if os.path.exists(filepath):
        return
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)


def download_txt(from_="", to="", urlparams=None):
    name = get_output_filename(os.path.basename(to))
    path = os.path.join(os.path.dirname(to), name)
    content = get_text_from_url(from_, urlparams)
    if content:
        save_book(path, content)


def print_book_details(details):
    print("\n==========")
    if details["title"]:
        print(f"=== Заголовок: {details['title']} ===")
    if details["author"]:
        print(f"=== Автор: {details['author']} ===")
    if details["comments"]:
        comments = "\n ".join(details["comments"])
        print(f"=== Комментарии: \n{comments} ===")
    if details["genres"]:
        print(f"=== Жанры: {details['genres']} ===")
    if details["img_url"]:
        print(f"=== Ссылка: {details['img_url']} ===")
    print("==========")


def save_image(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if os.path.exists(filepath):
        return
    with open(filepath, "wb") as file:
        file.write(content)


def download_image(from_="", to=""):
    if not from_ or not to:
        return
    content = get_content_from_url(from_)
    if content:
        save_image(to, content)


def make_description(json_dict, filepath="./books.json"):
    with open(filepath, "w", encoding="utf-8") as write_file:
        json.dump(json_dict, write_file, indent=4, ensure_ascii=False)
