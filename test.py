import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
import urllib


BASE_URL = "http://tululu.org"
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
        img = soup.find("div", class_="bookimage").find("img")
        if img:
            src = urllib.parse.urljoin(BASE_URL, img.get("src"))
        else:
            src = None
        return {"title": title, "author": author, "img_url": src}
    except AttributeError as e:
        print(e)
    except TypeError as e:
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


def check_or_make_dir(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.mkdir(dir)


def save_book(path, content):
    check_or_make_dir(path)
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
                    print(f"Заголовок. {info['title']} \n{info['img_url']}\n")
                    ext = info["img_url"].split(".")[-1]
                    save_image(f"{name}.{ext}", res.content)
            except Exception as e:
                print(e)


def save_image(name, content, folder="images"):
    filepath = os.path.join(os.getcwd(), folder, name)
    check_or_make_dir(filepath)
    if not os.path.exists(filepath):
        with open(filepath, "wb") as file:
            file.write(content)


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
    get_images_from_10_books()
