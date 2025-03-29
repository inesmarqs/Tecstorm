import os
from bs4 import BeautifulSoup
import requests
import re

class Product:
    def __init__(self, name, url, id, **kwargs):
        #kwargs can be any extra information that we might need
        self.name = name
        self.url = url
        self.id = id
        for key, value in kwargs.items():
            setattr(self, key, value)


def get_barcode_from_url(url):
    error_counter = 0
    while True:
        try:
            try:
                page_to_scrape = requests.get(url, timeout=error_counter+1)  
            except requests.exceptions.RequestException as e:
                print(f"Ocorreu um erro ao acessar a página: {e}")
                raise Exception

            try:
                soup = BeautifulSoup(page_to_scrape.text, 'html.parser')
            except UnboundLocalError as e:
                raise Exception(e)
            link = soup.find('a', attrs={'data-url': True})
            if link:
                data_url = link.get('data-url')

                match = re.search(r"ean=(\d+)", data_url)
                
                if match:
                    ean_number = match.group(1)
                    return ean_number
            
            raise Exception
        except Exception as e:
            error_counter += 1
            print(f"Ocorreu um erro ao extrair o EAN: erro #{error_counter}")
            if error_counter >= 4:
                return None

def main():
    curr_dir = os.getcwd()
    folder = os.path.join(curr_dir, "docs")
    files = os.listdir(folder)
    if "ids.txt" in files:
        os.remove("{}/ids.txt".format(folder))
    new_file = open("{}/ids.txt".format(folder), "a+")
    if "urls.txt" in files:
        for line in open("{}/urls.txt".format(folder), "r"):
            barcode = get_barcode_from_url(line[:-1])
            if barcode:
                new_file.write(barcode + "\n")
            print(f"Url {line} possui EAN: {barcode}")
    new_file.close()
    
if __name__ == "__main__":
    main()
            