import requests
from bs4 import BeautifulSoup


page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")
soup = BeautifulSoup(page.content, 'html.parser')

print([type(item) for item in list(soup.children)])