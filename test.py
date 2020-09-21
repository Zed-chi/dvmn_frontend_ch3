import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


BASE_BOOK_PAGE = "http://tululu.org/b"
BOOK_URL = "http://tululu.org/txt.php?id="


def get_book_details(html):
    soup = BeautifulSoup(html, "lxml")
    header = soup.find("div", id="content").find("h1").text
    title, author = map(lambda x: x.strip(), header.split("::"))
    return {"title": title, "author": author}


def get_output_filename(url, filename, folder="books/"):
    name = sanitize_filename(filename)
    path = os.path.normpath(os.path.join("./", folder, name))
    return path


def get_url_content(url):
    res = requests.get(url)
    if not res.history and res.ok:
        return res.text
    else:
        return None


def download_txt(url, name, folder="/books"):
    path = get_output_filename(url, name, folder)
    return path


# Примеры использования
url = "http://tululu.org/txt.php?id=1"

filepath = download_txt(url, "Алиби")
print(filepath)  # Выведется books/Алиби.txt

filepath = download_txt(url, "Али/би", folder="books/")
print(filepath)  # Выведется books/Алиби.txt

filepath = download_txt(url, "Али\\би", folder="txt/")
print(filepath)  # Выведется txt/Алиби.txt
