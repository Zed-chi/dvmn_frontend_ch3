import requests
import os



def get_url_content(url):
    res = requests.get(url, allow_redirects=False)
    if not res.history and res.ok:
        return res.text
    else:
        return None


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
