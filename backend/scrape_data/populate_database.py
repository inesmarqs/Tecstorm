import json
from sqlalchemy.orm import Session
from db_session import get_db
from database.models import Product, Ingredient, NutricionalInformation, Category
from database.commands_database import add_product, add_category, add_product_populate, add_ingredient, add_nutricional_info
from sqlalchemy.exc import IntegrityError

# Caminho para o ficheiro JSON
JSON_PATH = "scrape_data/database.json"

# Campos nutricionais que podem aparecer
NUTRI_KEYS = [
    "Energia", "Energia kcal", "Lípidos", "Ácidos gordos saturados",
    "Hidratos de carbono", "Açúcares", "Fibra", "Proteínas", "Sal"
]

def populate_database():
    db: Session = next(get_db())

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        produtos = json.load(f)

    for prod in produtos:
        try:
            # Criar categoria se não existir
            categoria_nome = prod.get("categoria") or "Sem Categoria"
            categoria = db.query(Category).filter_by(name=categoria_nome).first()
            if not categoria:
                categoria = add_category(db, categoria_nome)
            else:
                categoria = categoria.id
            
            barcode = prod.get("id")
            if prod.get("nome") != None:
                name = prod.get("nome")
            elif prod.get("name") != None:
                name = prod.get("name")
            else:
                name = "Sem Nome"
            url = prod.get("url")
            if prod.get("description") != None:
                description = prod.get("description")
            elif prod.get("descricao") != None:
                description = prod.get("descricao")
            else:
                description = "Sem Descricao"
            brand = prod.get("brand")
            price = prod.get("price") if prod.get("price") != None else 0.0
            reference_num = prod.get("reference_num")
            image = prod.get("image")
            ingredientes = prod.get("ingredientes")
            nutrientes_texto = prod.get("nutrientes_texto")
            atributos = prod.get("atributos")
            
            product = add_product_populate(db, barcode, name, url, description, brand, price, reference_num, image,atributos, categoria)
            
            try:
                for ingrediente in ingredientes.split(", "):
                    ingrediente = ingrediente.strip()
                    ingrediente = add_ingredient(db, product, ingrediente)
            except Exception as e:
                pass
            
            try:
                for nutriente in nutrientes_texto.split(", "):
                    nutriente = nutriente.strip() 
                    #nutriente in database is not consistent, so this should be implemented later
                    nutriente = add_nutricional_info(db, product, nutriente)
                
            except Exception as e:
                pass
             
        except IntegrityError as e:
            print(f"Erro ao adicionar produto {name}: {e.orig}")

if __name__ == "__main__":
    populate_database()
