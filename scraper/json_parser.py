import json
import os

def filter_json_lines(input_path="docs/urls.json", output_path="docs/urls_filtered.json"):
    filtered_objects = []
    
    # Open the file and read each JSON line
    with open(input_path, "r", encoding="utf-8") as infile:
        for line in infile:
            try:
                obj = json.loads(line)
                # Only keep the object if its "id" is not null
                if obj.get("id") is not None:
                    filtered_objects.append(obj)
            except json.JSONDecodeError:
                # Skip lines that are not valid JSON
                continue
    
    # Write the filtered objects back to a new file (or overwrite the original)
    with open(output_path, "w", encoding="utf-8") as outfile:
        for obj in filtered_objects:
            outfile.write(json.dumps(obj, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    filter_json_lines()
    # Optionally, replace the original file:
    # os.replace("docs/urls_filtered.json", "docs/urls.json")
