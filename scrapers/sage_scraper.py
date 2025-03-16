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

# Cargar variables de entorno
load_dotenv()  # Esta línea estaba faltando, necesaria para cargar las variables de .env

# Configurar carpeta de descargas
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "downloads/sage")
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Configurar opciones de Chrome
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
    
    # Cargar variables de entorno
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")
    
    if not EMAIL or not PASSWORD:
        print("❌ Error: Variables de entorno EMAIL y PASSWORD no están configuradas.")
        return
        
    LOGIN_URL = "https://journals-sagepub-com.crai.referencistas.com/action/doSearch?AllField=Computational+Thinking&startPage=2&target=default&content=articlesChapters&pageSize=100"

    # Iniciar WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(LOGIN_URL)
        time.sleep(3)

        # ----------------------------------- LOGIN -----------------------------------
        try:
            # Intentar encontrar el botón de login de Google
            google_login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "btn-google"))
            )
            google_login_button.click()
            time.sleep(3)

            # Cambiar al popup de Google para iniciar sesión
            main_window = driver.current_window_handle
            for handle in driver.window_handles:
                if handle != main_window:
                    driver.switch_to.window(handle)
                    break

            # Ingresar correo
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "identifierId"))
            )
            email_input.send_keys(EMAIL)
            email_input.send_keys(Keys.RETURN)
            time.sleep(2)

            # Ingresar contraseña
            password_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "Passwd"))
            )
            password_input.send_keys(PASSWORD)
            password_input.send_keys(Keys.RETURN)
            time.sleep(5)
            
            # Regresar a la ventana principal si es necesario
            if len(driver.window_handles) > 1:
                driver.switch_to.window(main_window)
            
            # Esperar a que se complete el inicio de sesión
            time.sleep(10)

        except Exception as e:
            print(f"❌ Error durante el inicio de sesión: {e}")
            driver.quit()
            return
        
        # ----------------------------------- Aceptar cookies -----------------------------------
        try:
            aceptCookies = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept Non-Essential Cookies')]"))
            )
            aceptCookies.click()
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ No se encontró el botón de cookies o ya fueron aceptadas: {e}")

        # ----------------------------------- ITERAR PÁGINAS -----------------------------------
        for page in range(1, 33):
            print(f"📄 Procesando página {page}")
            
            # Esperar a que la página cargue completamente
            time.sleep(5)
            
            try:
                # Seleccionar todos los resultados
                checkbox = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.ID, "action-bar-select-all"))
                )
                driver.execute_script("arguments[0].scrollIntoView();", checkbox)
                driver.execute_script("arguments[0].click();", checkbox)
                print(f"✅ Página {page}: Seleccionados todos los artículos")
                time.sleep(3)
            except Exception as e:  
                print(f"❌ Error al seleccionar resultados en página {page}: {e}")
                continue

            try:
                # Encontrar el botón "Export selected citations"
                export_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'export-citation')]"))
                )
                driver.execute_script("arguments[0].scrollIntoView();", export_button)
                actions = ActionChains(driver)
                actions.move_to_element(export_button).click().perform()
                print("✅ Botón de exportación clickeado correctamente")
                time.sleep(10)
            except Exception as e:
                print(f"❌ Error al hacer clic en el botón de exportación: {e}")
                continue

            try:
                # Seleccionar formato BibTeX del dropdown
                citation_dropdown = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "citation-format"))
                )
                select = Select(citation_dropdown)
                select.select_by_value("bibtex")
                print("✅ Formato BibTeX seleccionado correctamente")
                time.sleep(10)
            except Exception as e:
                print(f"❌ Error al seleccionar BibTeX: {e}")
                continue
                
            try:    
                # Hacer clic en el botón de descarga
                download_button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Download citation')]"))
                )
                driver.execute_script("arguments[0].scrollIntoView();", download_button)
                download_button.click()  # Esta línea estaba comentada en el original
                print("✅ Botón de descarga clickeado correctamente")
                time.sleep(5)  # Dar tiempo para que se complete la descarga
            except Exception as e:
                print(f"❌ Error al hacer clic en el botón de descarga: {e}")
                continue

            try:
                # Cerrar el diálogo de exportación
                close_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@alt, 'close')]"))
                )
                close_button.click()
                print("✅ Diálogo de exportación cerrado correctamente")
                time.sleep(2)
            except Exception as e:
                print(f"❌ Error al cerrar el diálogo: {e}")
                # Intentar continuar incluso si no se puede cerrar

            try:
                # Ir a la siguiente página
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'page-item__arrow--next')]/a"))
                )
                actions = ActionChains(driver)
                actions.move_to_element(next_button).click().perform()
                print(f"✅ Navegando a la página {page + 1}")
                time.sleep(5)  # Dar tiempo para que cargue la siguiente página
            except Exception as e:
                print(f"❌ Error al navegar a la siguiente página o fin de resultados: {e}")
                break  # Si no hay más páginas, salir del bucle

    except Exception as e:
        print(f"❌ Error general: {e}")
    finally:
        print("🔄 Finalizando scraper...")
        driver.quit()
        
if __name__ == "__main__":
    sage_scraper()