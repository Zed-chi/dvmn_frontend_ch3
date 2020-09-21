import requests
from bs4 import BeautifulSoup


url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
response = requests.get(url)
response.raise_for_status()
print(response.text)
soup = BeautifulSoup(response.text, 'lxml')
print(soup.prettify())
title_tag = soup.find('main').find('header').find('h1')
title_text = title_tag.text
soup.find('img', class_='attachment-post-image')['src']
post = sopu.find("div", class_="entry-content")
text = post.text