import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

path = "/usr/local/bin/chromedriver"

def scrape_barcode_info(barcode):
    url = f"https://www.barcodelookup.com/{barcode}"

    options = Options()
    # options.add_argument("--headless")  # Ativa se quiseres
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(path), options=options)
    data = {}

    try:
        driver.get(url)
        print(f"🧭 Página carregada: {url}")
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # ✅ Nome
        try:
            data["nome"] = soup.select_one("h4.product-title").text.strip()
        except:
            data["nome"] = None

        # ✅ Descrição
        try:
            data["descricao"] = soup.select_one("div.product-meta-data .product-text").text.strip()
        except:
            data["descricao"] = None

        # ✅ Ingredientes
        try:
            for block in soup.select("div.product-meta-data"):
                label = block.select_one("div.product-text-label")
                if label and "Ingredients:" in label.text:
                    data["ingredientes"] = label.select_one("span.product-text").text.strip()
        except:
            data["ingredientes"] = None

        # ✅ Nutrition Facts (inline)
        try:
            for block in soup.select("div.product-meta-data"):
                label = block.select_one("div.product-text-label")
                if label and "Nutrition Facts:" in label.text:
                    data["nutrientes_texto"] = label.select_one("span.product-text").text.strip()
        except:
            data["nutrientes_texto"] = None

        # ✅ Atributos (MPN, Model, ASIN, Size...)
        data["atributos"] = {}
        try:
            for li in soup.select("#product-attributes li"):
                span = li.select_one("span")
                if span and ":" in span.text:
                    k, v = span.text.split(":", 1)
                    data["atributos"][k.strip().lower()] = v.strip()
        except:
            pass

        # ✅ Detalhes extra (brand, etc.)
        try:
            for li in soup.select("ul.product-details-list li"):
                if ":" in li.text:
                    k, v = li.text.split(":", 1)
                    data[k.strip().lower()] = v.strip()
        except:
            pass

    finally:
        driver.quit()

    return data


# Teste
if __name__ == "__main__":
    barcode = "5449000133328"
    info = scrape_barcode_info(barcode)

    print("\n📦 Dados extraídos:\n" + "="*40)
    for k, v in info.items():
        print(f"{k}: {v}")
