import requests
from bs4 import BeautifulSoup

url = "http://tululu.org/b1/"
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'lxml')
header = soup.find("div", id="content").find("h1").text
title, author = map(lambda x: x.strip(), header.split("::"))
print(title, author)