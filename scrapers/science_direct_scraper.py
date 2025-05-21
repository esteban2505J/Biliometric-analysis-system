import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

# Configure Download Folder
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "downloads/science")
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Configure Chrome Options
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": os.path.abspath(DOWNLOAD_FOLDER),
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True,
    "profile.default_content_settings.popups": 0,
    "profile.default_content_setting_values.automatic_downloads": 1
})

def scrape_science_direct():
    """Scrapes ScienceDirect, downloads BibTeX files, and iterates through pages."""
    
    # Load environment variables
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")
    LOGIN_URL = "https://www-sciencedirect-com.crai.referencistas.com/search?qs=computational%20thinking"

    # Start WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(LOGIN_URL)
    time.sleep(3)

    # ----------------------------------- LOGIN -----------------------------------
    try:
        google_login_button = driver.find_element(By.ID, "btn-google")
        google_login_button.click()
        time.sleep(3)

        main_window = driver.current_window_handle
        for handle in driver.window_handles:
            if handle != main_window:
                driver.switch_to.window(handle)
                break

        email_input = driver.find_element(By.ID, "identifierId")
        email_input.send_keys(EMAIL)
        email_input.send_keys(Keys.RETURN)
        time.sleep(3)

        password_input = driver.find_element(By.NAME, "Passwd")
        password_input.send_keys(PASSWORD)
        password_input.send_keys(Keys.RETURN)
        time.sleep(15)

    except Exception as e:
        print(f"❌ Error during login: {e}")
        driver.quit()
        return

    # ----------------------------------- SELECT 100 RESULTS (ONLY ONCE) -----------------------------------
    try:
        results_100 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'show=100')]"))
        )
        results_100.click()
        print("✅ Results set to 100 per page!")
        time.sleep(2)
    except:
        print("⚠️ 100 results per page already selected or not found.")

    # ----------------------------------- PAGINATION & DATA EXTRACTION -----------------------------------
    try:
        pagination_text = driver.find_element(By.XPATH, "//ol[@id='srp-pagination']/li[1]").text
        total_pages = int(pagination_text.split(" of ")[1])
        print(f"✅ Total pages: {total_pages}")

        for page in range(1, total_pages + 1):  
            try:

                time.sleep(2)    

                # ✅ Select all results
                checkbox = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.ID, "select-all-results"))
                )
                driver.execute_script("arguments[0].scrollIntoView();", checkbox)
                driver.execute_script("arguments[0].click();", checkbox)
                print(f"✅ Page {page}: Selected all articles!")

                time.sleep(2)

                # ✅ Click "Export" button
                export_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "export-all-link-button"))
                )
                export_button.click()
                time.sleep(2)

                # ✅ Click "Export citation to BibTeX"
                bibtex_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Export citation to BibTeX')]]"))
                )
                bibtex_button.click()
                print("✅ BibTeX export started!")
                time.sleep(3)  # Wait for the download
    

                # ✅ Select all results
                checkbox = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.ID, "select-all-results"))
                )
                driver.execute_script("arguments[0].scrollIntoView();", checkbox)
                driver.execute_script("arguments[0].click();", checkbox)
                print(f"✅ Page {page}: Selected all articles!")

                time.sleep(2)

                # ✅ Click "Next Page" if available
                try:
                    next_page = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[@data-aa-name='srp-next-page']"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView();", next_page)
                    next_page.click()
                    print(f"✅ Moved to page {page + 1}")
                    time.sleep(3)

                except:
                    print("⚠️ No 'Next Page' button found. Reached last page.")
                    break  # Stop the loop

            except Exception as e:
                print(f"❌ Error on page {page}: {e}")
                break  # Stop the loop on error

    except Exception as e:
        print(f"❌ Error extracting pagination: {e}")

    # ✅ Close the driver **only after processing all pages**
    driver.quit()
    print("✅ Scraping complete!")

if __name__ == "__main__":
    scrape_science_direct()
