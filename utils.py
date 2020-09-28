import os
import requests
import urllib
import json
import re
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup


BASE_URL = "http://tululu.org"


def check_or_make_dir(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


def get_content_from_url(url, allow_redirects=False):
    res = requests.get(url, allow_redirects=allow_redirects)
    if res.status_code == 200:
        return res.content
    else:
        return None


def get_text_from_url(url, allow_redirects=False):
    res = requests.get(url, allow_redirects=allow_redirects)
    if res.status_code == 200:
        return res.text
    else:
        return None


def get_output_filename(filename):
    name = sanitize_filename(filename)
    path = os.path.normpath(name)
    return path


def get_id_from_book_url(link):
    res = re.search(r"b([0-9]+)", link)
    if res:
        return res.group(1)


def get_book_details(html):
    if not html:
        return None
    try:
        soup = BeautifulSoup(html, "lxml")
        header = soup.select("#content > h1")[0].text
        title, author = map(lambda x: x.strip(), header.split("::"))
        img = soup.select(".bookimage img")[0]
        if img:
            src = urllib.parse.urljoin(BASE_URL, img.get("src"))
        else:
            src = None
        comments = list(map(lambda x: x.text, soup.select(".texts span")))
        genres = list(
            map(lambda x: x.text, soup.select("#content > .d_book > a"))
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


def save_book(path, content):
    check_or_make_dir(path)
    if os.path.exists(path):
        return
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)


def download_txt(from_="", to=""):
    name = get_output_filename(os.path.basename(to))
    path = os.path.join(os.path.dirname(to), name)
    content = get_text_from_url(from_)
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


def save_image(name, content):
    check_or_make_dir(name)
    if os.path.exists(name):
        return
    with open(name, "wb") as file:
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
