import os
import re
import json
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

url_test = "https://www.continente.pt/produto/mostarda-com-mel-paladin-5046337.html"

class Product:
    def __init__(self, name, url, id, categories=None, nutritional_info=None, **kwargs):
        """
        name: Nome do produto
        url: URL do produto
        id: Normalmente o EAN
        categories: lista de categorias (breadcrumbs)
        nutritional_info: dicionário com informações nutricionais
        kwargs: quaisquer outros atributos (price, brand, etc.)
        """
        self.name = name
        self.url = url
        self.id = id
        self.categories = categories if categories else []
        self.nutritional_info = nutritional_info if nutritional_info else {}

        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __str__(self):
        info = [
            f"Nome: {self.name}",
            f"URL: {self.url}",
            f"EAN: {self.id}",
            f"Categorias: {self.categories}",
            f"Nutritional Info: {self.nutritional_info}"
        ]
        # Exibir também quaisquer atributos extras
        extras = [
            f"{key}: {value}"
            for key, value in self.__dict__.items() 
            if key not in ("name", "url", "id", "categories", "nutritional_info")
        ]
        return "\n".join(info) + "\n" + "\n".join(extras)

def get_barcode_from_url(url):
    """
    Fallback para extrair o EAN de um data-url que contenha 'ean=xxxxx'
    """
    try:
        page_to_scrape = requests.get(url, timeout=18)
    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro ao acessar a página: {e}")
        return None

    soup = BeautifulSoup(page_to_scrape.text, 'html.parser')
    link = soup.find('a', attrs={'data-url': True})
    if link:
        data_url = link.get('data-url', '')
        match = re.search(r"ean=(\d+)", data_url)
        if match:
            return match.group(1)
    return None

def parse_breadcrumbs(soup):
    """
    Tenta encontrar a lista de breadcrumbs (categorias).
    Ajuste o seletor de acordo com a estrutura real do site.
    """
    categories = []
    # Tente localizar <nav> ou <ol> / <ul> com classe breadcrumb
    breadcrumb_items = soup.select('nav.breadcrumb ol li, ol.breadcrumb li, ul.breadcrumb li, nav.breadcrumb li')
    # Se não achar, tente algo mais específico dependendo do HTML real
    if not breadcrumb_items:
        breadcrumb_items = soup.find_all('li', class_='breadcrumb-item')
    
    for item in breadcrumb_items:
        link = item.find('a')
        if link:
            categories.append(link.get_text(strip=True))
        else:
            # às vezes o último item do breadcrumb não é um link
            categories.append(item.get_text(strip=True))
    
    # Remove possíveis vazios e duplicados
    categories = [cat for cat in categories if cat]
    return categories

def parse_nutritional_info(soup):
    """
    Captura informações nutricionais, por exemplo:
    - Tamanho da porção (serving-size, serving-size-uom)
    - Tabela de nutrientes (nutrients-table)
    Retorna um dicionário com esses dados.
    """
    nutritional_info = {}
    
    # Localiza a div principal de informação nutricional
    nutritional_area = soup.find('div', class_='nutritional-information-area')
    if not nutritional_area:
        return nutritional_info
    
    # 1) Tamanho de porção
    serving_size = nutritional_area.find('div', class_='serving-size')
    if serving_size:
        nutritional_info['serving_size'] = serving_size.get_text(strip=True)
    
    serving_size_uom = nutritional_area.find('div', class_='serving-size-uom')
    if serving_size_uom:
        nutritional_info['serving_size_uom'] = serving_size_uom.get_text(strip=True)
    
    # 2) Tabela de nutrientes
    nutrients_table = nutritional_area.find('div', class_='nutrients-table')
    if nutrients_table:
        # Pode ser que haja uma <table> dentro dessa div
        table = nutrients_table.find('table')
        if table:
            rows = table.find_all('tr')
        else:
            # Se não houver <table>, às vezes há <div> ou <p> com a info
            rows = nutrients_table.find_all('tr')  # ajuste se necessário

        table_data = {}
        for row in rows:
            # Normalmente, cada linha tem duas células: nome do nutriente e valor
            cells = row.find_all(['th', 'td'])
            if len(cells) == 2:
                key = cells[0].get_text(strip=True)
                value = cells[1].get_text(strip=True)
                table_data[key] = value
        
        nutritional_info['nutrients'] = table_data
    
    return nutritional_info

def get_product_info_from_url(url):
    """
    Extrai informações do produto a partir da página usando JSON-LD (dados estruturados),
    breadcrumbs (para categoria) e HTML (para info nutricional).
    Retorna um objeto Product com os dados coletados.
    """
    try:
        response = requests.get(url, timeout=18)
    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro ao acessar a página: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # -------------------------------------------------------------
    # 1) Extrair dados via JSON-LD
    # -------------------------------------------------------------
    product_data = None
    scripts = soup.find_all("script", type="application/ld+json")
    for script in scripts:
        try:
            json_data = json.loads(script.string)
            # Se o JSON for uma lista, itera para encontrar um item com @type "Product"
            if isinstance(json_data, list):
                for item in json_data:
                    if isinstance(item, dict) and item.get("@type") == "Product":
                        product_data = item
                        break
            elif isinstance(json_data, dict) and json_data.get("@type") == "Product":
                product_data = json_data
        except (json.JSONDecodeError, TypeError):
            continue
        if product_data:
            break

    # -------------------------------------------------------------
    # 2) Extrair breadcrumbs (categorias)
    # -------------------------------------------------------------
    categories = parse_breadcrumbs(soup)

    # -------------------------------------------------------------
    # 3) Extrair informações nutricionais (HTML)
    # -------------------------------------------------------------
    nutritional_info = parse_nutritional_info(soup)

    # -------------------------------------------------------------
    # 4) Construir objeto Product
    # -------------------------------------------------------------
    if product_data:
        # Dados básicos do JSON-LD
        name = product_data.get("name")
        description = product_data.get("description")
        brand = None
        if "brand" in product_data:
            if isinstance(product_data["brand"], dict):
                brand = product_data["brand"].get("name")
            else:
                brand = product_data["brand"]
        
        # EAN via fallback (JSON-LD nem sempre tem "gtin13")
        ean = get_barcode_from_url(url)

        offers = product_data.get("offers", {})
        price = offers.get("price")
        reference_num = product_data.get("sku")
        image = product_data.get("image")  # se quiser armazenar
        if ean == None:
            print("EAN not found")
            return None
        return Product(
            name=name,
            url=url,
            id=ean,
            categories=categories,
            nutritional_info=nutritional_info,
            description=description,
            brand=brand,
            price=price,
            reference_num=reference_num,
            image=image
        )
    else:
        # Se não encontrou dados estruturados, extrai ao menos EAN
        ean = get_barcode_from_url(url)
        return Product(
            name=None,
            url=url,
            id=ean,
            categories=categories,
            nutritional_info=nutritional_info
        )

def process_url(url):
    """
    Função auxiliar para processar uma única URL.
    Retorna uma tupla (url, product) onde product é None em caso de erro.
    """
    product = get_product_info_from_url(url)
    return url, product

def load_processed_urls(output_file):
    processed = set()
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            for line in f:
                try:
                    product = json.loads(line)
                    if product.get("url"):
                        processed.add(product["url"])
                except Exception as e:
                    # Optionally, log or handle errors in parsing JSON lines
                    continue
    return processed

def main():
    folder = os.path.join(os.getcwd(), "docs")
    urls_file = os.path.join(folder, "urls.txt")
    output_file = os.path.join(folder, "urls.json")
    error_file_path = os.path.join(folder, "errors.txt")
    
    if os.path.exists(error_file_path):
        os.remove(error_file_path)
    
    # Load already processed URLs
    processed_urls = load_processed_urls(output_file)
    
    # Leia todas as URLs e filtra as já processadas
    with open(urls_file, "r") as f:
        urls = ["https://www.continente.pt/produto/cesto-acrilico-cinza-escuro-kasa-397299.html"]
    
    # Usando ThreadPoolExecutor para processar URLs em paralelo
    max_workers = 15  # Ajuste o número de threads conforme necessário
    with ThreadPoolExecutor(max_workers=max_workers) as executor, \
         open(output_file, "a+") as new_file, \
         open(error_file_path, "a+") as error_file:
        
        # Submete todas as tarefas
        future_to_url = {executor.submit(process_url, url): url for url in urls}
        
        # Processa os resultados conforme vão completando
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                url_result, product = future.result()
                if product or product:
                    new_file.write(json.dumps(product.__dict__) + "\n")
                    print(f"Url {url_result} possui EAN: {product.id}")
                else:
                    error_file.write(url + "\n")
                    print(f"Falta de EAN: {url}")
            except Exception as e:
                error_file.write(url + "\n")
                print(f"Exceção ao processar URL {url}: {e}")

if __name__ == "__main__":
    main()
