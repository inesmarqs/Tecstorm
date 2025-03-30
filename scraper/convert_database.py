


file1 = open("docs/database.json", "r")
file2 = open("docs/urls_to_use.txt", "r")
animal = open("docs/animais.txt", "r")
bebidas = open("docs/bebidas-e-garrafeira.txt", "r")
bio = open("docs/bio-eco-e-saudavel.txt", "r")
casa = open("docs/casa-bricolage-e-jardim.txt", "r")
congelados = open("docs/congelados.txt", "r")
desporto = open("docs/desporto-e-malas-de-viagem.txt", "r")
frescos = open("docs/frescos.txt", "r")
laticinios = open("docs/laticinios-e-ovos.txt", "r")
limpeza = open("docs/limpeza.txt", "r")
mercearia = open("docs/mercearia.txt", "r")

categorias = [
    animal,
    bebidas,
    bio,
    casa,
    congelados,
    desporto,
    frescos,
    laticinios,
    limpeza,
    mercearia
]

dicionario = {}

def parse_produto_lines(lines):
    import re

    parsed_data = []
    all_keys = set()

    raw_parsed = []

    for line in lines:
        line = line.strip()
        atributos = line.split(", ")

        produto = {}
        for attr in atributos:
            if ": " in attr:
                chave, valor = attr.split(": ", 1)
                chave = chave.strip()
                valor = valor.strip().strip("'").strip("‘").strip("’")
                produto[chave] = valor
                all_keys.add(chave)
        raw_parsed.append(produto)

    # Preencher os campos em falta com None
    full_data = []
    for item in raw_parsed:
        full_item = {key: item.get(key, None) for key in sorted(all_keys)}
        full_data.append(full_item)

    return full_data

with open("docs/urls_to_use.txt", "r", encoding="utf-8") as f:
    linhas = f.readlines()

produtos = parse_produto_lines(linhas)

# Ver primeiro produto
print(produtos[0])

    
