import requests
from bs4 import BeautifulSoup

r = requests.get("https://www.youtube.com/results?search_query=python+web+scraping")

soup = BeautifulSoup(r.text, "html.parser")

# for link in soup.find_all("a"):
#     print(link.get("href"))

print(soup.get_text())