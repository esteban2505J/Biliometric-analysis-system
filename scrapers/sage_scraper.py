import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

# Configure Download Folder
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "downloads/sage")
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

def sage_scraper():
    """Scrapes ScienceDirect, downloads BibTeX files, and iterates through pages."""
    
    # Load environment variables
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")
    LOGIN_URL = "https://journals-sagepub-com.crai.referencistas.com/action/doSearch?AllField=Computational+Thinking&startPage=2&target=default&content=articlesChapters&pageSize=200"

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
        time.sleep(2)

        password_input = driver.find_element(By.NAME, "Passwd")
        password_input.send_keys(PASSWORD)
        password_input.send_keys(Keys.RETURN)
        time.sleep(20)

    except Exception as e:
        print(f"❌ Error during login: {e}")
        driver.quit()
    
    # ----------------------------------- acept cookies -----------------------------------

    aceptCookies = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept Non-Essential Cookies')]"))
        )
    
    aceptCookies.click()

    time.sleep(2)

    # ----------------------------------- SELECT 200 RESULTS (ONLY ONCE) -----------------------------------
    try:
        for page in range(1,16):
                
            # ✅ Select all results
            checkbox = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.ID, "action-bar-select-all"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", checkbox)
            driver.execute_script("arguments[0].click();", checkbox)
            print(f"✅ Page {page}: Selected all articles!")

            time.sleep(2)

            #✅  Find the "Export selected citations" button
            export_button = driver.find_element(By.XPATH, "//a[contains(@class, 'export-citation')]")

            # Scroll into view if necessary
            driver.execute_script("arguments[0].scrollIntoView();", export_button)

            # Click the button
            actions = ActionChains(driver)
            actions.move_to_element(export_button).click().perform()

            print("✅ Export button clicked successfully!")

            time.sleep(3)
            try:
                #✅ Locate the dropdown element
                citation_dropdown = WebDriverWait(driver,10).until(
                        EC.presence_of_element_located((By.ID, "citation-format"))
                )
                    
                # Select BibTeX
                select = Select(citation_dropdown)
                select.select_by_value("bibtex")  # ✅ Selecting BibTeX directly

                print("✅ BibTeX format selected successfully!")
                time.sleep(3)

            except Exception as e:
                print("❌ Error selecting BibTeX:", e)
                
            #✅ Locate the download button
            try:
                download_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Download citation')]"))
                )
                # driver.execute_script("arguments[0].scrollIntoView();", download_button)
                download_button.click()

                print("✅ Download button clicked successfully!")
            except Exception as e:
                print("❌ Error clicking download button:", e)

            time.sleep(5)    

            close_button = driver.find_element(By.XPATH, "//button[@data-dismiss='modal']")
            driver.execute_script("arguments[0].click();", close_button)

                
            try:

                #✅ go to next page
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'page-item__arrow--next')]/a"))
                )

                # Click the "Next" button
                actions = ActionChains(driver)
                actions.move_to_element(next_button).click().perform()
                print("Next page clicked!")
            except Exception as e:
                print("❌ Error clicking next page:", e)

         

    except Exception as e:
        print(f"❌ Error during login: {e}")
        driver.quit()
        return
        
if __name__ == "__main__":
    sage_scraper()