from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import Client, Product, Ingredient, Allergen, NutricionalInformation, ShoppingCart


# ------------- INSERT COMMANDS -------------

def add_client(db: Session, name: str, telephone: str, creditcard: str, birth_date: str):
    """Adds a client to the database."""
    db_client = Client(name=name, telephone=telephone, creditcard=creditcard, birth_date=birth_date)
    db.add(db_client)
    db.commit()
    return db_client.id


def add_product(db: Session, bar_code: str, name: str, brand: str, price: float, weight: float, store_location: str, nutricional_info_id: int):
    """Adds a product to the database."""
    db_product = Product(
        bar_code=bar_code, name=name, brand=brand, price=price, weight=weight, 
        store_location=store_location, nutricional_information_id=nutricional_info_id
    )
    db.add(db_product)
    db.commit()
    return db_product.id


def add_ingredient(db: Session, product_id: int, name: str):
    """Adds an ingredient to the database."""
    db_ingredient = Ingredient(product_id=product_id, name=name)
    db.add(db_ingredient)
    db.commit()
    return db_ingredient.id


def add_allergen(db: Session, client_id: int, name: str):
    """Adds an allergen to the database."""
    db_allergen = Allergen(client_id=client_id, name=name)
    db.add(db_allergen)
    db.commit()
    return db_allergen.id


def add_nutricional_info(db: Session, energy_kj: float, energy_kcal: float, lipids: float, 
                         saturated_lipids: float, carbon_hidrats: float, sugar_carbon_hidrats: float, 
                         fiber: float, protein: float, salt: float):
    """Adds nutritional information to the database."""
    db_info = NutricionalInformation(
        energy_kj=energy_kj, energy_kcal=energy_kcal, lipids=lipids, saturated_lipids=saturated_lipids, 
        carbon_hidrats=carbon_hidrats, sugar_carbon_hidrats=sugar_carbon_hidrats, fiber=fiber, 
        protein=protein, salt=salt
    )
    db.add(db_info)
    db.commit()
    return db_info.id

def add_shopping_cart(db: Session, client_id: int, product_id: int):
    """Adds shopping cart information to the database."""
    db_info = ShoppingCart(client_id=client_id, product_id=product_id)
    db.add(db_info)
    db.commit()
    return db_info.id

# ------------- GET COMMANDS -------------

def get_client(db: Session, client_id: int):
    """Retrieves a client by ID."""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


def get_product(db: Session, product_id: int):
    """Retrieves a product by ID."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


def get_ingredients_by_product(db: Session, product_id: int):
    """Retrieves all ingredients for a given product."""
    ingredients = db.query(Ingredient).filter(Ingredient.product_id == product_id).all()
    if not ingredients:
        raise HTTPException(status_code=404, detail="No ingredients found for this product")
    return ingredients


def get_allergens_by_client(db: Session, client_id: int):
    """Retrieves all allergens for a given client."""
    allergens = db.query(Allergen).filter(Allergen.client_id == client_id).all()
    if not allergens:
        raise HTTPException(status_code=404, detail="No allergens found for this client")
    return allergens


def get_nutricional_info(db: Session, nutricional_info_id: int):
    """Retrieves nutritional information by ID."""
    nutricional_info = db.query(NutricionalInformation).filter(NutricionalInformation.id == nutricional_info_id).first()
    if not nutricional_info:
        raise HTTPException(status_code=404, detail="Nutritional information not found")
    return nutricional_info

def get_shopping_cart_by_client(db: Session, client_id: int):
    """Retrieves all products ids in shopping cart for a given client."""
    carts = db.query(ShoppingCart).filter(ShoppingCart.client_id==client_id).all()
    if not carts:
        raise HTTPException(status_code=404, detail="Shopping Cart not found")
    return carts