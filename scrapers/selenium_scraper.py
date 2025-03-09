import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bibtexparser import loads

# Configuración
EMAIL = os.getenv("EMAIL")
PASSWORD =  os.getenv("PASSWORD")
LOGIN_URL = "https://www-sciencedirect-com.crai.referencistas.com/search?qs=computational%20thinking"
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "downloads")

# Crear carpeta de descargas si no existe
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Configurar opciones de Chrome
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": DOWNLOAD_FOLDER,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

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
        time.sleep(120)  # Esperar redirección después del login
    except Exception as e:
        print(f"Error en el proceso de login de Google: {e}")


def download_bibtex():
    """Find and click the BibTeX download button."""
    try:
        time.sleep(2)  # Wait for the page to load

        check = driver.find_element(By.ID, "select-all-results")
        

         # Use JavaScript to click the checkbox
        driver.execute_script("arguments[0].click();", check)

        time.sleep(2)

        openModal = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".button-link.export-all-link-button"))
    )   
        openModal.click()

        time.sleep(2)

        downloadBibtex = WebDriverWait(driver,2).until(
            EC.element_to_be_clickable((By.CLASS_NAME, ".button-link-text"))
        )    

        downloadBibtex.click()



        print("✅ Download initiated...")

        # Wait for download confirmation
        time.sleep(5)  # Adjust this based on the site's behavior

    except Exception as e:
        print(f"❌ Error downloading BibTeX: {e}")


def wait_for_download():
    """Espera hasta que el archivo BibTeX aparezca en la carpeta de descargas"""
    timeout = 30
    start_time = time.time()
    while time.time() - start_time < timeout:
        files = [f for f in os.listdir(DOWNLOAD_FOLDER) if f.endswith(".bib")]
        if files:
            print("Archivo BibTeX descargado.")
            return
        time.sleep(1)
    print("Tiempo de espera agotado. No se encontró el archivo.")

def process_bibtex():
    """Busca y procesa el archivo BibTeX más reciente"""
    files = [f for f in os.listdir(DOWNLOAD_FOLDER) if f.endswith(".bib")]
    if not files:
        print("No se encontraron archivos BibTeX.")
        return
    latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(DOWNLOAD_FOLDER, f)))
    bib_path = os.path.join(DOWNLOAD_FOLDER, latest_file)
    with open(bib_path, "r", encoding="utf-8") as bibtex_file:
        bib_database = loads(bibtex_file.read())
    for entry in bib_database.entries:
        print(f"Título: {entry.get('title', 'N/A')}")
        print(f"Autores: {entry.get('author', 'N/A')}")
        print(f"Año: {entry.get('year', 'N/A')}")
        print(f"DOI: {entry.get('doi', 'N/A')}")
        print("-" * 40)

if __name__ == "__main__":
    try:
        login()
        download_bibtex()
        process_bibtex()
    finally:
        driver.quit()
