from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def scrape_dynamic_site(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)  # Wait for JavaScript to load

    articles = driver.find_elements(By.CLASS_NAME, "article")
    data = [{"title": art.text} for art in articles]
    
    driver.quit()
    return data

if __name__ == "__main__":
    url = "https://example.com/js-research"
    data = scrape_dynamic_site(url)
    print(data)
