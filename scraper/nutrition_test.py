import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.continente.pt/produto/mostarda-com-mel-paladin-5046337.html"

def main():
    # Ajuste o caminho do chromedriver:
    path_chromedriver = "/usr/local/bin/chromedriver"
    
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Se quiser rodar em modo headless (sem abrir janela do navegador):
    # chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(service=Service(path_chromedriver), options=chrome_options)

    try:
        driver.get(URL)
        
        # Aguarda o carregamento básico da página (por exemplo, o título do produto)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.product-name"))
        )

        # Tenta fechar banner de cookies, se existir
        time.sleep(2)
        try:
            # Exemplo 1: remover o overlay
            cookie_overlay = driver.find_element(By.ID, "CybotCookiebotDialogBodyUnderlay")
            driver.execute_script("arguments[0].remove();", cookie_overlay)
            
            # Exemplo 2: clicar no botão "Aceitar" (caso exista)
            # accept_btn = driver.find_element(By.CSS_SELECTOR, "button#CybotCookiebotDialogBodyButtonAccept")
            # accept_btn.click()
        except:
            pass

        print("Página carregada!")
        # Espera o container de abas aparecer
        tabs_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-description-accordion"))
        )
        print("Container de abas encontrado!")
        
        # Localiza todas as abas (botões) - verifique se a classe confere no HTML real
        tab_buttons = tabs_container.find_elements(By.CSS_SELECTOR, "button.product-description-accordion-title")
        
        # Dicionário para guardar o conteúdo de cada aba
        tabs_content = {}

        # Clica em cada aba e extrai o conteúdo
        for btn in tab_buttons:
            tab_title = btn.text.strip()
            print(f"\n--- Clicando na aba: {tab_title} ---")

            # Faz scroll até o botão (para garantir que o clique seja possível)
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            time.sleep(1)
            btn.click()
            time.sleep(2)  # Tempo para o JS expandir a aba

            # Depois de expandir, o conteúdo costuma aparecer numa div logo depois do <button>
            content_div = btn.find_element(By.XPATH, "following-sibling::div[@class='product-description-accordion-content']")
            
            # Captura o texto ou HTML
            aba_html = content_div.get_attribute("innerHTML")
            aba_text = content_div.text

            tabs_content[tab_title] = {
                "html": aba_html,
                "text": aba_text
            }

        # Exibe (ou processa) as informações de cada aba
        for title, content in tabs_content.items():
            print(f"\n=== Conteúdo da aba: {title} ===")
            print(content["text"])
            
            # Se precisar de parse adicional com BeautifulSoup, por exemplo:
            soup = BeautifulSoup(content["html"], "html.parser")
            # A partir daqui, você pode buscar tags específicas, classes, etc.
            # Exemplo: print(soup.get_text(separator=" ", strip=True))

    except Exception as e:
        print("Erro:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
