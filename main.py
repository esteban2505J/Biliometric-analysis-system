import requests
from bs4 import BeautifulSoup

url = "https://www.example.com/articles"
headers = {"User-Agent": "Mozilla/5.0"}  # Helps avoid blocks

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

articles = soup.find_all("h2", class_="article-title")
for article in articles:
    title = article.text.strip()
    link = article.find("a")["href"]
    print(f"Title: {title}, Link: {link}")
