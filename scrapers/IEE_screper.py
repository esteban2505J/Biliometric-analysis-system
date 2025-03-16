import os
import time
from dotenv import load_dotenv
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Configure Download Folder
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "downloads/IEE")
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

chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--disable-software-rasterizer")  # Prevents Chrome from using software rendering
chrome_options.add_argument("--no-sandbox")  # Sometimes helps with GPU issues



def scrape_IEE():

    """Scrapes IEE, downloads BibTeX files, and iterates through pages."""
    
    # Load environment variables
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")
    LOGIN_URL = "https://ieeexplore-ieee-org.crai.referencistas.com/search/searchresult.jsp?newsearch=true&queryText=Computational%20thinking&highlight=true&returnType=SEARCH&matchPubs=false&rowsPerPage=10&pageNumber=1&returnFacets=ALLhttps://www-sciencedirect-com.crai.referencistas.com/search?qs=computational%20thinking"

    # Start WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(LOGIN_URL)
    time.sleep(3)

    try:
        google_login_button = driver.find_element(By.ID, "btn-google")
        google_login_button.click()
        time.sleep(3)

        main_window = driver.current_window_handle
        for handle in driver.window_handles:
            if handle != main_window:
                driver.switch_to.window(handle)
                break

        email_input = WebDriverWait(driver,3).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
            
        email_input.send_keys(EMAIL)
        email_input.send_keys(Keys.RETURN)
        time.sleep(3)

        password_input = driver.find_element(By.NAME, "Passwd")
        password_input.send_keys(PASSWORD)
        password_input.send_keys(Keys.RETURN)
        time.sleep(15)

    except Exception as e:
        print(f"❌ Error during login: {e}")
        import traceback
        print(traceback.format_exc()) 
   
      
    
    # --------------------------------- acept cookies------------------------------------------------------------

    button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.osano-cm-accept-all")))
    button.click()

        

    time.sleep(5)

    # --------------------------------- select 100 items per page------------------------------------------------------------   

    try:
        itemsPerPage = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "dropdownPerPageLabel")))   

        itemsPerPage.click()

        # Esperar a que aparezcan las opciones y seleccionar la que tiene "100"
        option_100 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '100')]"))
        )
        option_100.click()

        # Confirmar la selección (opcional)
        print("Seleccionaste 100 elementos por página.")

        time.sleep(5)
    except Exception as e:
        print(f"❌ Error select 100: {e}")
        import traceback
        print(traceback.format_exc()) 
    

    # --------------------------------- extract the data ------------------------------------------------------------
    try:
        for i in range(1,30):
            
            print(f"📄 Procesando página {i}...")

            # ✅ Select all results
            checkbox = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "results-actions-selectall-checkbox"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", checkbox)
            driver.execute_script("arguments[0].click();", checkbox)  

            time.sleep(2)
                
            # ✅ Select export results
            export = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Export')]"))
            )
            export.click()

            time.sleep(2)
             # ✅ Select "Citation" option
            citations_tab = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Citations')]"))
            )
            citations_tab.click()

                
            # ✅ Select BibTeX format
            bibtex_radio = WebDriverWait(driver,5).until(
                EC.element_to_be_clickable((By.XPATH, "//label[@for='download-bibtex']/input"))
                )


            if not bibtex_radio.is_selected():
                bibtex_radio.click()
            time.sleep(2)

            # ✅ Add abstract to the file
            add_abstract = WebDriverWait(driver, 10).until(
                 EC.element_to_be_clickable((By.XPATH, "//label[contains(., 'Citation and Abstract')]/input")))
            if not add_abstract.is_selected():
                add_abstract.click()

            time.sleep(2)
                
            # ✅ Slect "download" button
                    # Locate the download button by its class name
            try:
                download_button = driver.find_element(By.CLASS_NAME, "stats-SearchResults_Citation_Download")
                # Scroll to the button if it's not visible
                driver.execute_script("arguments[0].scrollIntoView();", download_button)
                
                # Click the button
                download_button.click()
                print("Download button clicked successfully!")
            except Exception as e:
                print("Error clicking download button:", e)

            time.sleep(10)

            # ✅ Close the download window
            try:
                  # Wait until the close button is clickable
                close_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[i[contains(@class, 'fa-times')]]"))
                )

                # Use ActionChains to click
                actions = ActionChains(driver)
                actions.move_to_element(close_button).click().perform()
            except Exception as e:
                print("Error clicking close button:", e)

              # ✅ Select all results
            checkbox = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "results-actions-selectall-checkbox"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", checkbox)
            driver.execute_script("arguments[0].click();", checkbox)  

            time.sleep(2)
            

            time.sleep(2)
                
            # ✅ Select next page
            try:
                next_page = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.CLASS_NAME, "stats-Pagination_arrow_next_2"))
                )
                next_page.click()
                time.sleep(2)
            except Exception:
                print("No hay más páginas disponibles.")
            time.sleep(2)
    except Exception as e:
        print(f"❌ Error during extract data: {e}")    
      

    driver.quit()

if __name__ == "__main__":
    scrape_IEE()