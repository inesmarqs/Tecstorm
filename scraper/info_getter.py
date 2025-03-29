from bs4 import BeautifulSoup
import requests
import json
import tempfile
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url_test = "https://www.continente.pt/produto/leite-uht-meio-gordo-continente-6879912.html"
path = "/usr/local/bin/chromedriver"

def get_info_from_url(url):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    with tempfile.TemporaryDirectory() as user_data_dir:
        options.add_argument(f"--user-data-dir={user_data_dir}")
        try:
            driver = webdriver.Chrome(service=Service(path), options=options)
        except Exception as e:
            print("Erro ao iniciar o ChromeDriver:", e)
            return None
        
        try:
            driver.get(url)
            print("Página carregada:", url)
        except Exception as e:
            print("Erro ao carregar a URL:", url, e)
            driver.quit()
            return None
        
        while True:
            driver.execute_script(
                "var content = document.getElementById('CybotCookiebotDialogBodyContent');"
                "if(content){ content.remove(); }"
                "var underlay = document.getElementById('CybotCookiebotDialogBodyUnderlay');"
                "if(underlay){ underlay.remove(); }"
            )
            
            try:
                element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".row.no-gutters.js-product-tabs--wrapper")))
                eleme

            except Exception as e:
                print("Erro ao carregar a URL:", url, e)
                driver.quit()
                return None

            return driver
            # class="row no-gutters js-product-tabs--wrapper"
            
            
print(get_info_from_url(url_test))