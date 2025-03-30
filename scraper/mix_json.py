import json
import os

def read_file_as_lines(path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return []
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()

def parse_json_lines(lines):
    json_objects = []
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            json_objects.append(obj)
        except json.JSONDecodeError:
            print(f"❌ Erro ao converter JSON na linha {i+1}")
    return json_objects

# Caminhos
ines_path = "docs/merged_clean_urls.json"
temp_path = "docs/temp_new_urls.json"
output_path = "docs/new_merged_clean_urls.json"

# Lê os ficheiros linha a linha
ines_lines = read_file_as_lines(ines_path)
temp_lines = read_file_as_lines(temp_path)

# Faz o parsing de cada linha como JSON individual
ines_data = parse_json_lines(ines_lines)
temp_data = parse_json_lines(temp_lines)

print(f"📦 {len(ines_data)} itens lidos de merged_clean_urls.json")
print(f"📦 {len(temp_data)} itens lidos de temp_new_urls.json")

# Elimina duplicados por 'ean'
merged_dict = {}
for item in ines_data + temp_data:
    ean = item.get("id")
    print(f"📦 {ean}")
    if ean:
        merged_dict[ean] = item

merged = list(merged_dict.values())

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print(f"✅ {len(merged)} produtos únicos guardados em '{output_path}'")
