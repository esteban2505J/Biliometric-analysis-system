import os
import time
import random
from dotenv import load_dotenv
from selenium import webdriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ✅ Ruta de descarga personalizada
DOWNLOAD_FOLDER = r"C:\Users\newUs\Documents\uni\projects\bibliometricProject\downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)  # ✅ Asegura que el directorio exista

# Configuración de opciones de Chrome
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # ✅ Oculta WebDriver
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--incognito")  # ✅ Modo incógnito
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")  # ✅ Agregar User-Agent

# ✅ Configuración de preferencias de descarga
prefs = {
    "download.default_directory": DOWNLOAD_FOLDER,  # ✅ Define la carpeta de descargas
    "download.prompt_for_download": False,  # ✅ No preguntar antes de descargar
    "download.directory_upgrade": True,  # ✅ Permite cambiar directorio de descarga
    "safebrowsing.enabled": True,  # ✅ Activa la navegación segura
    "profile.default_content_setting_values.automatic_downloads": 1  # ✅ Permite descargas automáticas
}
chrome_options.add_experimental_option("prefs", prefs)


def human_delay(base_time=2):
    """ Introduce un retraso aleatorio para simular comportamiento humano """
    time.sleep(base_time + random.uniform(0.5, 1.5))


def scrape_other_website():
    """ Scrapea la web y descarga archivos en la ruta especificada """

    LOGIN_URL = "https://dl.acm.org/action/doSearch?AllField=Computational+Thinking"

    # ✅ Iniciar el driver de Chrome no detectado
    driver = uc.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")  # ✅ Oculta WebDriver
    
    driver.get(LOGIN_URL)
    human_delay()

    try:
        # Aceptar Cookies
        permit_all_cookies = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
        )
        driver.execute_script("arguments[0].click();", permit_all_cookies)
        human_delay()

        # Esperar y hacer clic en la opción de "50" resultados por página
        link_50 = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'pageSize=50')]"))
        )
        link_50.click()
        print("✅ Click en '50' resultados por página.")

        result_text = 0

        while result_text < 3000:

            human_delay(2)

            # Esperar a que aparezca el texto "Mostrando 1 - 50"
            result_text = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//span[@class='result__current']/span"))
            ).text

            last_number = int(result_text.split()[-1])  # Extraer '50' y convertirlo en int
            print(f"✅ Número extraído: {last_number} (tipo: {type(last_number)})")

            # Seleccionar Checkbox
            checkbox = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.NAME, "markall"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", checkbox)
            human_delay(1)
            driver.execute_script("arguments[0].click();", checkbox)

            print("✅ Checkbox marcado.")

            # Abrir modal de exportación
            open_modal = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@title='Export Citations']"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", open_modal)
            human_delay()
            driver.execute_script("arguments[0].click();", open_modal)

            print("✅ Modal de exportación abierto.")

            # Exportar como BibTeX
            export_bibtex = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@title='Download citation']"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", export_bibtex)
            human_delay()
            driver.execute_script("arguments[0].click();", export_bibtex)

            print("✅ Descarga iniciada.")

            human_delay(3)  # Esperar la descarga

            # Siguiente página
            next_page_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@class='pagination__btn--next']"))
            )
            driver.execute_script("arguments[0].click();", next_page_button)
            print("✅ Pasando a la siguiente página.")

    except Exception as e:
        print(f"⚠️ Error durante la ejecución: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    scrape_other_website()
