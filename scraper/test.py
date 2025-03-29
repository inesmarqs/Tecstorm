import time
import json
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

website = "https://www.continente.pt"
categorias = [
    "desporto-e-malas-de-viagem",
]

path = "/usr/local/bin/chromedriver"

def scrape(category_url, wait_time=30, categoria=None):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    product_links = set()
    with tempfile.TemporaryDirectory() as user_data_dir:
        options.add_argument(f"--user-data-dir={user_data_dir}")
        try:
            driver = webdriver.Chrome(service=Service(path), options=options)
        except Exception as e:
            print("Erro ao iniciar o ChromeDriver:", e)
            return list(product_links)

        try:
            driver.get(category_url)
            print("Página carregada:", category_url)
        except Exception as e:
            print("Erro ao carregar a URL:", category_url, e)
            driver.quit()
            return list(product_links)

        print(f"Iniciando paginação para a categoria: {category_url}")

        while True:
            # Remover possíveis banners de cookies
            driver.execute_script(
                """
                var content = document.getElementById('CybotCookiebotDialogBodyContent');
                if(content){ content.remove(); }
                var underlay = document.getElementById('CybotCookiebotDialogBodyUnderlay');
                if(underlay){ underlay.remove(); }
                """
            )

            # Ler contagem atual e total de produtos, se disponível
            current_count, total_count = 0, 0
            try:
                counter_text = driver.find_element(By.CSS_SELECTOR, "div.search-results-products-counter").text
                parts = counter_text.split(" de ")
                if len(parts) >= 2:
                    current_count_str = parts[0].strip()
                    total_count_str = parts[1].split()[0].strip()
                    current_count = int(current_count_str)
                    total_count = int(total_count_str)
                    print(f"Produtos carregados: {current_count} de {total_count}")
            except Exception as ex:
                print("Não foi possível ler o contador de produtos:", ex)

            # Se já carregou todos os produtos ou não conseguiu ler contagem, encerra
            if total_count > 0 and current_count >= total_count:
                print("Todos os produtos foram carregados.")
                break

            # Tentar encontrar e clicar no botão "Ver mais produtos"
            try:
                more_button = WebDriverWait(driver, wait_time).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.search-view-more-products-button"))
                )
                # Rolando especificamente até o botão, para não "perder" o clique
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", more_button)
                time.sleep(1)  # Pequena pausa para garantir que a rolagem aconteceu
                more_button.click()
                time.sleep(2)  # Esperar carregamento dos novos produtos
            except Exception as e:
                print("Botão 'Ver mais produtos' não encontrado ou não está clicável:", e)

                # Após tentar clicar, verificamos a contagem novamente.
                # Se ainda não carregou tudo, mas não encontramos o botão, provavelmente
                # ele está fora de alcance ou a página não carrega mais produtos.
                try:
                    if total_count > 0 and current_count < total_count:
                        print("Ainda há produtos para carregar, mas o botão não está disponível.")
                    else:
                        print("Não há mais produtos ou não foi possível carregar mais.")
                except Exception as ex:
                    print("Erro ao checar contagem após falha no clique:", ex)

                # Encerra o loop se não for possível avançar
                break

        # Coletar todos os links de produtos após carregar tudo
        try:
            WebDriverWait(driver, wait_time).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, 'a[href^="/produto"], a[href^="https://www.continente.pt/produto"]')
                )
            )
        except Exception as e:
            print("Erro ao carregar os produtos:", e)

        products = driver.find_elements(By.CSS_SELECTOR, 'a[href^="/produto"], a[href^="https://www.continente.pt/produto"]')
        
        # Salvar em arquivo (um por categoria, caso queira)
        file = open(f"{categoria}.txt", "w", encoding="utf-8")
        for product in products:
            href = product.get_attribute("href")
            if href:
                if href.startswith('/'):
                    href = website + href
                product_links.add(href)
                file.write(href + "\n")
        file.close()

        driver.quit()
    return list(product_links)


def main():
    results = {}
    for categoria in categorias:
        category_url = f"{website}/{categoria}"
        print("\nIniciando scraping para a categoria:", category_url)
        links = scrape(category_url, wait_time=30, categoria=categoria)
        results[categoria] = links
        print(f"Total de links coletados para '{categoria}': {len(links)}")
    
    # Salva os resultados em um arquivo JSON
    with open("urls.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    print("Resultados salvos em urls.json")

if __name__ == "__main__":
    main()
    print("Done")
