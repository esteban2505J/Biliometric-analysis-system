import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuración
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
LOGIN_URL = "https://www-sciencedirect-com.crai.referencistas.com/search?qs=computational%20thinking"



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

# Crear carpeta de descargas si no existe
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)


# Iniciar WebDriver
driver = webdriver.Chrome(options=chrome_options)

def login():
    """ Función para autenticarse en ScienceDirect usando Google """
    driver.get(LOGIN_URL)
    time.sleep(3)  # Esperar a que cargue la página

    try:
        # Hacer clic en el botón "Iniciar sesión con Google"
        google_login_button = driver.find_element(By.ID, "btn-google")
        google_login_button.click()
        time.sleep(3)  # Esperar a que aparezca la ventana de Google
    except Exception as e:
        print(f"Error al hacer clic en el botón de Google: {e}")
        return

    # Cambiar a la nueva ventana emergente de Google (si existe)
    main_window = driver.current_window_handle
    for handle in driver.window_handles:
        if handle != main_window:
            driver.switch_to.window(handle)
            break

    try:
        # Introducir el email
        email_input = driver.find_element(By.ID, "identifierId")
        email_input.send_keys(EMAIL)
        email_input.send_keys(Keys.RETURN)
        time.sleep(3)  # Esperar a que cargue la página de contraseña

        # Introducir la contraseña
        password_input = driver.find_element(By.NAME, "Passwd")
        password_input.send_keys(PASSWORD)
        password_input.send_keys(Keys.RETURN)
        time.sleep(15)  # Esperar redirección después del login
    except Exception as e:
        print(f"Error en el proceso de login de Google: {e}")

def download_bibtex():
    """Find and click the BibTeX download button."""
    try:
        driver.current_url

        time.sleep(2)  # Wait for the page to load
        checkbox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "select-all-results"))
        )

        # Scroll to the checkbox
        driver.execute_script("arguments[0].scrollIntoView();", checkbox)

         # Click the checkbox using JavaScript to ensure it works
        driver.execute_script("arguments[0].click();", checkbox)
    
        print("✅ Checkbox clicked successfully!")

        # Wait for the "Export" button to be clickable
        export_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "export-all-link-button"))
        )

        # Scroll to the button to ensure visibility
        driver.execute_script("arguments[0].scrollIntoView();", export_button)

        # Click the button
        export_button.click()

        print("✅ Export button clicked successfully!")

        time.sleep(2)


            # Wait for the modal and the BibTeX button to appear
        bibtex_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Export citation to BibTeX')]]"))
        )

        # Scroll into view (just in case)
        driver.execute_script("arguments[0].scrollIntoView();", bibtex_button)

        # Click the button
        bibtex_button.click()

        print("✅ BibTeX export button clicked successfully!")

        print("✅ Download initiated...")

        # Wait for download confirmation
        time.sleep(5)  # Adjust this based on the site's behavior

    except Exception as e:
        print(f"❌ Error downloading BibTeX: {e}")


def wait_for_download():
    """Espera hasta que el archivo BibTeX aparezca en la carpeta de descargas"""
    print("is arriving at this function")
    timeout = 30
    start_time = time.time()
    while time.time() - start_time < timeout:
        files = [f for f in os.listdir(DOWNLOAD_FOLDER) if f.endswith(".bib")]
        if files:
            print("Archivo BibTeX descargado.")
            return
        time.sleep(1)
    print("Tiempo de espera agotado. No se encontró el archivo.")


if __name__ == "__main__":
    try:
        login()
        download_bibtex()
        wait_for_download()
    finally:
        driver.quit()
