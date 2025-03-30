import json
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
INPUT_JSON = "docs/urls2.json"
OUTPUT_JSON = "docs/urls_enriched.json"
OUTPUT_PARTIAL_JSON = "docs/urls_enriched_partial.json"
MID_SAVE = "docs/temp_new_urls.json"

def scrape_barcode_info(barcode):
    url = f"https://www.barcodelookup.com/{barcode}"

    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)
    scraped = {"id": barcode}

    try:
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        def try_select(selector):
            el = soup.select_one(selector)
            return el.text.strip() if el else None

        scraped["nome"] = try_select("h4.product-title")
        scraped["descricao"] = try_select("div.product-meta-data .product-text")

        scraped["ingredientes"] = None
        for block in soup.select("div.product-meta-data"):
            label = block.select_one("div.product-text-label")
            if label and "Ingredients:" in label.text:
                scraped["ingredientes"] = label.select_one("span.product-text").text.strip()
                break

        scraped["nutrientes_texto"] = None
        for block in soup.select("div.product-meta-data"):
            label = block.select_one("div.product-text-label")
            if label and "Nutrition Facts:" in label.text:
                scraped["nutrientes_texto"] = label.select_one("span.product-text").text.strip()
                break

        scraped["nutrientes"] = {}
        for row in soup.select("table.nutrition tr"):
            cols = row.find_all("td")
            if len(cols) == 2:
                label = cols[0].text.strip()
                value = cols[1].text.strip()
                scraped["nutrientes"][label] = value

        scraped["atributos"] = {}
        for li in soup.select("#product-attributes li span"):
            if ":" in li.text:
                k, v = li.text.split(":", 1)
                scraped["atributos"][k.strip()] = v.strip()
                
        # ✅ Detalhes extra (brand, etc.)
        try:
            for li in soup.select("ul.product-details-list li"):
                if ":" in li.text:
                    k, v = li.text.split(":", 1)
                    scraped[k.strip().lower()] = v.strip()
        except:
            pass

    except Exception as e:
        scraped["erro_scraping"] = str(e)

    finally:
        driver.quit()

    # Guardar no ficheiro intermédio (checkpoint)
    with open(MID_SAVE, "a+", encoding="utf-8") as f:
        f.write(json.dumps(scraped, ensure_ascii=False) + "\n")

    return scraped

def main():
    produtos = []

    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            for obj in data:
                if "id" in obj and obj["id"]:
                    produtos.append(obj)
        except Exception as e:
            print(f"❌ Erro a ler {INPUT_JSON}: {e}")


    # Ler IDs já presentes no MID_SAVE
    ids_already_scraped = set()
    if os.path.exists(MID_SAVE):
        with open(MID_SAVE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    ids_already_scraped.add(obj["id"])
                except:
                    continue

    all_ids = list({p["id"] for p in produtos if "id" in p})
    ids_to_scrape = [pid for pid in all_ids if pid not in ids_already_scraped]

    total = len(all_ids)
    remaining_to_scrape = len(ids_to_scrape)
    counter = 0

    print(f"🔄 A processar {remaining_to_scrape} novos de {total} totais (já processados: {len(ids_already_scraped)})...\n")

    with ThreadPoolExecutor(max_workers=14) as executor:
        futures = {executor.submit(scrape_barcode_info, pid): pid for pid in ids_to_scrape}
        for future in as_completed(futures):
            result = future.result()
            counter += 1
            if result.get("nome"):  # Só guarda se tiver nome
                with open(OUTPUT_PARTIAL_JSON, "a", encoding="utf-8") as f:
                    f.write(json.dumps(result, ensure_ascii=False) + "\n")
            print(f"✅ [{counter}/{remaining_to_scrape}] {result['id']} - {result.get('nome')} | Faltam: {remaining_to_scrape - counter}")

if __name__ == "__main__":
    main()
