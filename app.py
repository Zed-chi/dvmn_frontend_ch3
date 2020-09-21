import requests
import os
from dotenv import load_dotenv


load_dotenv()
books_folder = os.getenv("books_folder", "/books/")
file_url = "http://tululu.org/b32168/"
base_txt_url = "http://tululu.org/txt.php?id="


def get_book(url):
    res = requests.get(url, allow_redirects=False)
    if res.status_code == 200:
        return res.text
    else:
        raise Exception("Url is Corrupted")


def init():
    path = os.path.join(os.getcwd(), books_folder)
    print(path)
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception as e:
            print(e)


def save_book(path, filename, data):
    try:
        with open(f"{path}/{filename}", "w", encoding="utf-8") as file:
            file.write(data)
    except Exception as e:
        print(e)


def main():
    init()
    for i in range(1, 10):
        try:
            data = get_book(f"{base_txt_url}{i}")
            save_book(
                os.path.join(os.getcwd(), books_folder), f"id{i}.txt", data
            )
        except Exception as e:
            print(e)
    print("Downloading Finished")


if __name__ == "__main__":
    main()
