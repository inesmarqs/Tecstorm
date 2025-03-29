"""Consults the database and prints all the data in the shopwise database."""
from database.models import Client, NutricionalInformation, Product, Ingredient, Allergen, ShoppingCart
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./shopwise.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def print_all_clients():
    """Prints all the clients in the shopwise database."""
    db = SessionLocal()
    try:
        clients = db.query(Client).all()
        print("--------------------------------------------------------------\Clients:")
        for client in clients:
            print(f"Client ID: {client.id},"
                  f"Client Name: {client.name},"
                  f"Client Telephone: {client.telephone},"
                  f"Client CreditCard: {client.credit_card},"
                  f"Client Birth Date: {client.birth_date},"
                  f"Client Password: {client.password}"
                )
    finally:
        db.close()

def print_all_shopping_carts():
    """Prints all shopping carts in the shopwise database"""
    db = SessionLocal()
    try:
        carts = db.query(ShoppingCart).all()
        print("-------------------------------------------------------------\Shopping Carts:")
        for cart in carts:
            print(f"Shopping Cart ID: {cart.id},"
                  f"Shooping Cart Client ID: {cart.client_id},"
                  f"Shooping Cart Product ID: {cart.product_id}"
                  )
    finally:
        db.close()

def print_all_allergens():
    """Prints all the allergens in the shopwise database."""
    db = SessionLocal()
    try:
        allergens = db.query(Allergen).all()
        print("--------------------------------------------------------------\nAllergens:")
        for allergen in allergens:
            print(f"Allergen ID: {allergen.id},"
                  f"Allergen Client ID: {allergen.client_id}, "
                  f"Allergen Name: {allergen.name}"
                )
    finally: 
        db.close()

def print_all_products():
    """Prints all the products in the shopwise database."""
    db = SessionLocal()
    try:
        products = db.query(Product).all()
        print("--------------------------------------------------------------\Products:")
        for product in products:
            print(f"Product ID: {product.id}, "
                  f"Product Bar Code: {product.bar_code}, "
                  f"Product Name: {product.name}, "
                  f"Product Brand: {product.brand}, "
                  f"Product Price: {product.price}, "
                  f"Product Weight: {product.weight}, "
                  f"Product Store Location: {product.store_location}"
                  )
    finally:
        db.close()

def print_all_ingredients():
    """Prints all the ingredients in the shopwise database."""
    db = SessionLocal()
    try:
        ingredients = db.query(Ingredient).all()
        print("--------------------------------------------------------------\Ingredients:")
        for ingredient in ingredients:
            print(f"Ingredient ID: {ingredient.id}, " 
                  f"Ingredient Product ID: {ingredient.product_id}, " 
                  f"Ingredient Name: {ingredient.name}" 
            )
                  
    finally:
        db.close()


def print_all_nutricional_information():
    """Prints all the nutricional information in the shopwise database."""
    db = SessionLocal()
    try:
        informations = db.query(NutricionalInformation).all()
        print("--------------------------------------------------------------\Nutricional Informations:")
        for information in informations:
            print(f"Nutricional Information ID: {information.id}, "
                  f"Product ID: {information.product_id}, "
                  f"Energy KJ: {information.energy_kj}, "
                  f"Energy KCal: {information.energy_kcal}, "
                  f"Lipids: {information.lipids}, "
                  f"Saturated Lipids: {information.saturated_lipids}, "
                  f"Carbon Hidrats: {information.carbon_hidrats}, "
                  f"Sugar Carbon Hidrats: {information.sugar_carbon_hidrats}, "
                  f"Fiber: {information.fiber}, "
                  f"Protein: {information.protein}, "
                  f"Salt: {information.salt}")
    finally:
        db.close()

if __name__ == "__main__":
    print_all_clients();
    print_all_allergens();
    print_all_products();
    print_all_ingredients();
    print_all_nutricional_information();