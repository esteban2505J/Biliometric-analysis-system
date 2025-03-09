import requests
from bs4 import BeautifulSoup

def scrape_webpage(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("div", class_="article")
        data = [{"title": art.find("h2").text, "authors": art.find("span", class_="author").text} for art in articles]
        return data
    else:
        print(f"Failed to scrape {url}")
        return []

if __name__ == "__main__":
    url = "https://example.com/research"
    scraped_data = scrape_webpage(url)
    print(scraped_data)
