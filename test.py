import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


BASE_BOOK_PAGE = "http://tululu.org/b"
BOOK_URL = "http://tululu.org/txt.php?id="


def download_10_books():
    for id in range(1, 11):
        download_txt_from_tululu_by_id(id)


def get_book_details(html):
    if not html:
        return None
    try:
        soup = BeautifulSoup(html, "lxml")
        header = soup.find("div", id="content").find("h1").text
        title, author = map(lambda x: x.strip(), header.split("::"))
        return {"title": title, "author": author}
    except AttributeError as e:
        print(e)


def get_output_filename(filename, folder="books/"):
    name = sanitize_filename(filename)
    path = os.path.normpath(os.path.join("./", folder, name))
    return path


def get_url_content(url, allow_redirects=False):
    res = requests.get(url, allow_redirects=allow_redirects)
    if res.status_code == 200:
        return res.text
    else:
        return None


def save_book(path, content):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.mkdir(dir)
    with open(path, "w") as file:
        file.write(content)


def download_txt(url, name, folder="/books"):
    path = get_output_filename(url, name, folder)
    return path


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


"""
# Примеры использования
url = "http://tululu.org/txt.php?id=1"

filepath = download_txt(url, "Алиби")
print(filepath)  # Выведется books/Алиби.txt

filepath = download_txt(url, "Али/би", folder="books/")
print(filepath)  # Выведется books/Алиби.txt

filepath = download_txt(url, "Али\\би", folder="txt/")
print(filepath)  # Выведется txt/Алиби.txt
"""
if __name__ == "__main__":
    download_10_books()
