import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



DOWNLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "downloads")  # ✅ Ensure correct path

chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": os.path.abspath(DOWNLOAD_FOLDER),  # ✅ Ensure absolute path
    "download.prompt_for_download": False,  # ✅ Disable Save As dialog
    "download.directory_upgrade": True,  # ✅ Allow changing directories
    "safebrowsing.enabled": True,  # ✅ Enable safe browsing
    "profile.default_content_settings.popups": 0,  # ✅ Disable pop-ups
    "profile.default_content_setting_values.automatic_downloads": 1  # ✅ Allow multiple downloads
})


def scrape_other_website():
    """Scrapes another website with different logic."""
   

    LOGIN_URL = "https://dl.acm.org/action/doSearch?AllField=Computational+Thinking"

    
    # Iniciar WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(LOGIN_URL)

    permitAllCokies = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
        )

    permitAllCokies.click()
    time.sleep(2)


    checkbox = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.NAME, "markall"))
    )

    try:
        
        # Scroll to the checkbox
        driver.execute_script("arguments[0].scrollIntoView();", checkbox)

        # Click the checkbox using JavaScript to ensure it works
        driver.execute_script("arguments[0].click();", checkbox)

    except Exception as e:

        print(f"Error al hacer clic en el botón de Google: {e}")
        return

    time.sleep(3)
    
    print("✅ Checkbox clicked successfully!")

    opeModal = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@title='Export Citations']"))
    )

     # Scroll to the checkbox
    driver.execute_script("arguments[0].scrollIntoView();", opeModal)

    # Click the checkbox using JavaScript to ensure it works
    driver.execute_script("arguments[0].click();", opeModal)

    print("✅ Clicked 'Export Citations' link successfully!")

    time.sleep(2)

    exportBibtex = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@title='Download citation']"))
    )

     # Scroll to the checkbox
    driver.execute_script("arguments[0].scrollIntoView();", exportBibtex)

    # Click the checkbox using JavaScript to ensure it works
    driver.execute_script("arguments[0].click();", exportBibtex)

    print("✅ Clicked 'Export Citations' link successfully!")
    time.sleep(2)
   
    driver.quit()
   



        

   

    driver.quit()

if __name__ == "__main__":
    scrape_other_website()