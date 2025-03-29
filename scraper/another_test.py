import requests
from bs4 import BeautifulSoup
import json

url = "https://www.continente.pt/produto/mostarda-com-mel-paladin-5046337.html"
response = requests.get(url, timeout=5)
soup = BeautifulSoup(response.text, "html.parser")

# Encontra todas as tags que possuem JSON-LD
scripts = soup.find_all("script", type="application/ld+json")
for idx, script in enumerate(scripts, start=1):
    try:
        data = json.loads(script.string)
        print(f"--- JSON-LD {idx} ---")
        print(json.dumps(data, indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"Erro ao processar JSON-LD {idx}: {e}")