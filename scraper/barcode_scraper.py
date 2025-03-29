import requests
from bs4 import BeautifulSoup
import re  
import os

categorias = [
    "frescos",
    "laticinios-e-ovos",
    "congelados",
    "mercearia",
    "bebidas-e-garrafeira",
    "bio-eco-e-saudavel",
    "limpeza",
    "beleza-e-higiene",
    "bebe",
    "animais",
    "casa-bricolage-e-jardim",
    "brinquedos-e-jogos",
    "livraria-e-papelaria",
    "desporto-e-malas-de-viagem",
]

base = "https://www.continente.pt/"

def get_barcode_from_url(url):
    try:
        page_to_scrape = requests.get(url, timeout=1)  
    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro ao acessar a página: {e}")

    try:
        soup = BeautifulSoup(page_to_scrape.text, 'html.parser')
    except UnboundLocalError as e:
        return None

    link = soup.find('a', attrs={'data-url': True}) 

    if link:
        data_url = link.get('data-url')

        match = re.search(r"ean=(\d+)", data_url)
        
        if match:
            ean_number = match.group(1)
            print(f"Url {url} possui EAN: {ean_number}")
            return ean_number
    
    return None

def get_all_urls_category(category):
    url = base + category
    try:
        page_to_scrape = requests.get(url, timeout=1)  
    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro ao acessar a página: {e}")
        return []
        
    soup = BeautifulSoup(page_to_scrape.text, 'html.parser')
    
    print("tentar categoria ", category)
    
    links = soup.find_all('a', attrs={'href': True})
    print(f"categoria {category} analisada")
    print(f"Total de URLs encontradas: {len(links)}")
    file = open(f"{category}.txt", "w")
    for link in links:
        file.write(link.get('href') + "\n")
    file.close()
    
    return [base + link.get('href') for link in links]

def get_all_urls():
    try:
        page_to_scrape = requests.get(base, timeout=1)
    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro ao acessar a página: {e}")
        return []
    
    soup = BeautifulSoup(page_to_scrape.text, 'html.parser')
    
    links = soup.find_all('a', attrs={'href': True})
    file = open("urls.txt", "w")
    for link in links:
        file.write(link.get('href') + "\n")
    file.close()
    
    urls = [base + link.get('href') for link in links]
    return urls

def main():
    urls = get_all_urls()
    print(f"Total de URLs encontradas: {len(urls)}")


if __name__ == "__main__":
    main()