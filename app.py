import requests

file_url = "http://tululu.org/b32168/"
txt_url = "http://tululu.org/txt.php?id=32168"

def get_book(url):
    res = requests.get(url)
    return res.text

if __name__ == "__main__":
    data = get_book(txt_url)
    print(data)
