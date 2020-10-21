import json
import os
import re
import urllib

from bs4 import BeautifulSoup

from pathvalidate import sanitize_filepath

import requests


BASE_URL = "https://tululu.org"


def get_content_from_url(url, allow_redirects=False):
    response = requests.get(url, allow_redirects=allow_redirects)
    response.raise_for_status()
    return response.content


def get_text_from_url(url, urlparams=None, allow_redirects=False):
    response = requests.get(
        url,
        allow_redirects=allow_redirects,
        params=urlparams,
    )
    response.raise_for_status()
    return response.text


def get_id_from_book_url(url):
    result = re.search(r"b([0-9]+)", url)
    if not result:
        raise LookupError(f"Cant get book id from {url}")
    return result.group(1)


def get_book_details(html, base_url):
    soup = BeautifulSoup(html, "lxml")
    header = soup.select_one("#content > h1").text
    title, author = [text.strip() for text in header.split("::")]
    img = soup.select_one(".bookimage img")
    src = urllib.parse.urljoin(base_url, img.get("src"))
    comments = [tag.text for tag in soup.select(".texts span")]
    genres = [tag.text for tag in soup.select("#content > .d_book > a")]

    return {
        "title": title,
        "author": author,
        "img_url": src,
        "comments": comments,
        "genres": genres,
    }


def save_book(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if os.path.exists(filepath):
        raise FileExistsError(f"Book {filepath} already saved")
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)


def download_txt(from_="", to="", urlparams=None):
    path = sanitize_filepath(to)
    content = get_text_from_url(from_, urlparams)
    if not content:
        raise ValueError(f"Got empty textfile from {from_}")
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
        raise FileExistsError(f"Image {filepath} is already saved.")
    with open(filepath, "wb") as file:
        file.write(content)


def download_image(from_=None, to=None):
    path = sanitize_filepath(to)
    content = get_content_from_url(from_)
    if not content:
        raise ValueError(f"Got empty image from {from_}")
    save_image(path, content)


def make_description(json_dict, filepath="./books.json"):
    with open(filepath, "w", encoding="utf-8") as write_file:
        json.dump(json_dict, write_file, indent=4, ensure_ascii=False)
