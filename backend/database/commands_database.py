from sqlalchemy.orm import Session
from fastapi import HTTPException
from database.models import Client, Product, Ingredient, Allergen, NutricionalInformation, ShoppingCart, Category, Recommendations
from db_session import get_db
from sqlalchemy.exc import IntegrityError



# ------------- INSERT COMMANDS -------------

def add_client(db: Session, name: str, telephone: str, credit_card: str, birth_date: str, password:str):
    """Adds a client to the database."""
    db_client = Client(name=name, telephone=telephone, credit_card=credit_card, birth_date=birth_date, password=password)
    db.add(db_client)
    db.commit()
    return db_client.id


def add_product(db: Session, bar_code: str, name: str, brand: str, price: float, weight: float, store_location: str, category_id: int):
    """Adds a product to the database."""
    db_product = Product(
        bar_code=bar_code, name=name, brand=brand, price=price, weight=weight, 
        store_location=store_location, category_id=category_id   
        )
    db.add(db_product)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        print("Produto já existente, ignorado.")
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
                         fiber: float, protein: float, salt: float, product_id: int):
    """Adds nutritional information to the database."""
    db_info = NutricionalInformation(
        energy_kj=energy_kj, energy_kcal=energy_kcal, lipids=lipids, saturated_lipids=saturated_lipids, 
        carbon_hidrats=carbon_hidrats, sugar_carbon_hidrats=sugar_carbon_hidrats, fiber=fiber, 
        protein=protein, salt=salt, product_id=product_id
    )
    db.add(db_info)
    db.commit()
    return db_info.id

def add_shopping_cart(db: Session, client_id: int, product_id: int, uid: int, success: bool):
    """Adds shopping cart information to the database."""
    db_info = ShoppingCart(client_id=client_id, product_id=product_id, uid=uid, success=success)
    db.add(db_info)
    db.commit()
    return db_info.id

def add_category(db: Session, name: str):
    """Adds a category to the database."""
    db_category = Category(name=name)
    db.add(db_category)
    db.commit()
    return db_category.id

def remove_shopping_cart(db: Session, client_id: int, product_id: int, uid: int):
    
    print(f"🧹 Removendo item: {client_id}, {product_id}, {uid}")
    deleted = db.query(ShoppingCart).filter(
        ShoppingCart.client_id == client_id,
        ShoppingCart.product_id == product_id,
        ShoppingCart.uid == uid
    ).delete()

    db.commit()

    print(f"🧹 Itens apagados: {deleted}")

    return

def add_recommendations(db, client_id, product_id, product_recommended_id):
    db = next(get_db()) 
    db_info = Recommendations(client_id=client_id, product_id=product_id, product_recommended_id=product_recommended_id)
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

def get_product_by_barcode(db: Session, bar_code: str):
    """Retrieves a product by bar code."""
    product = db.query(Product).filter(Product.bar_code == bar_code).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def get_category(db: Session, category_id: int):
    """Retrieves a category by ID."""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


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

def get_product_by_barcode(db: Session, barcode: int):
    """Retrieved the product given a bar code"""
    product = db.query(Product).filter(Product.bar_code==barcode).one()
    if not product: 
        raise HTTPException(status_code=404, detail="Product not found for this bar code.")
    return product

def get_product_by_category(db: Session, category_id: int):
    """Retrieved the product given a category"""
    product = db.query(Product).filter(Product.category_id==category_id).all()
    if not product: 
        raise HTTPException(status_code=404, detail="Product not found for this category.")
    return product

def get_product_by_category_without_blacklisted(db: Session, category_id: int, problem_id: int):
    """Retrieved the product given a category"""
    product = db.query(Product).filter(Product.category_id==category_id, Product.id != problem_id).all()
    if not product: 
        raise HTTPException(status_code=404, detail="Product not found for this category.")
    return product

def get_shopping_cart_items(db: Session, client_id: int):
    """Retrieved every shopping cart product"""
    product = db.query(ShoppingCart).filter(ShoppingCart.client_id==client_id).all()
    if not product: 
        raise HTTPException(status_code=404, detail="Product not found in the shopping cart")
    return product

def get_shopping_cart_item_by_uid(db: Session, uid: int):
    """Retrieved shopping cart product by uid tag"""
    product = db.query(ShoppingCart).filter(ShoppingCart.uid==uid).all()
    if not product:
        raise HTTPException(status_code=404, detail="Product was not in the cart")
    return product

def get_recommendations_by_product_id(db: Session, product_id: int, client_id:int):
    """Retrieved recommendations given a failed product id"""
    recommendation = db.query(Recommendations).filter(Recommendations.product_id==product_id and Recommendations.client_id==client_id).one()
    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return recommendation
#-----------------------DELETE COMMANDS------------------------

def delete_shopping_cart_items(db: Session, client_id: int):
    """Deletes all items in the shopping cart for a given client."""
    try:
        db.query(ShoppingCart).filter(ShoppingCart.client_id == client_id).delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        db.rollback()  
        raise e
    
def delete_recommendations(db: Session, client_id: int):
    """Deletes all recommendation entries for a given client."""
    try:
        db.query(Recommendations).filter(Recommendations.client_id == client_id).delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        db.rollback()  
        raise e