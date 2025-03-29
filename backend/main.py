import asyncio
import os
import shutil
from pathlib import Path
import ai_services
from database.database import SessionLocal
from fastapi import Depends, FastAPI, File, HTTPException, Request, UploadFile, Header, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from database.models import Client, Product, Allergen, Ingredient, NutricionalInformation
from sqlalchemy.orm import Session
import json
import paho.mqtt.client as mqtt
import threading

from database.commands_database import (
    add_client,
    add_allergen,
    add_ingredient,
    add_category,
    add_nutricional_info,
    add_product,
    add_shopping_cart,
    get_allergens_by_client,
    get_client,
    get_category,
    get_ingredients_by_product,
    get_nutricional_info,
    get_product,
    get_shopping_cart_by_client,
    get_product_by_barcode, 
    get_product_by_category,
    get_product_by_category_without_blacklisted,
    delete_shopping_cart_items
)

app = FastAPI()
MQTT_BROKER = "test.mosquitto.org"  # Public broker
MQTT_PORT = 1883
MQTT_TOPIC = "test/topic"
 
# Create an MQTT client instance
mqtt_client = mqtt.Client()

def get_db():
    """_get_db_.

    Yields:
        Session: SQLAlchemy session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def populate_db():
    db = next(get_db())
    category = add_category(db, "frutas")
    
    client_id = add_client(db, "user1", "915193363", "22222222222", "12-12-1980", "password")
    shopping_cart = add_shopping_cart(db, client_id, 1)
    allergens = add_allergen(db, client_id, "gluten")
    
    nutricion1 = add_nutricional_info(db,
        energy_kj = 100,
        energy_kcal = 50,
        lipids = 10,
        saturated_lipids = 5,
        carbon_hidrats = 20,
        sugar_carbon_hidrats = 10,
        fiber = 5,
        protein = 10,
        salt = 0,
        product_id = 1
    )

    print("2")
    ingredient1 = Ingredient(
        id = 1,
        product_id = 1,
        name = "gluten"
    )
    
    print("3")
    product = Product(
        id = 1,
        bar_code = "123456789",
        name = "laranja",
        brand = "laranja",
        price = 1.99,
        weight = 1.0,
        store_location = "a1",
    )
    print("Try to add")
    
    add_product(db, bar_code=product.bar_code, name=product.name, brand=product.brand, price=product.price, weight=product.weight, store_location=product.store_location, category_id=category)
    add_product(db, bar_code="123456781", name="banana", brand="banana", price=1.99, weight=1.0, store_location="a1", category_id=category)
    add_product(db, bar_code="123444444", name="cherry", brand="cherry", price=1.99, weight=1.0, store_location="a1", category_id=category)
    add_product(db, bar_code="666632342", name="apple", brand="apple", price=1.99, weight=1.0, store_location="a1", category_id=category)
    add_product(db, bar_code="123453212", name="tangerine", brand="tangerine", price=1.99, weight=1.0, store_location="a1", category_id=category)
    add_product(db, bar_code="123450089", name="grape", brand="grape", price=1.99, weight=1.0, store_location="a1", category_id=category)
    add_ingredient(db, product.id, "gluten")
    add_ingredient(db, 1, "orange")
    add_ingredient(db, 2, "banana")
    add_ingredient(db, 3, "cherry")
    add_ingredient(db, 4, "apple")
    add_ingredient(db, 5, "orange")
    add_ingredient(db, 6, "grape")
    add_nutricional_info(db,
        energy_kj = 100,
        energy_kcal = 50, lipids=10, saturated_lipids=5, carbon_hidrats=20, sugar_carbon_hidrats=10, fiber=5, protein=10, salt=0, product_id=1)
        
def example_data():
    print("1")
    db = next(get_db())
    check = get_product(db, 1)
    print(check)
    client = get_client(db, 1)
    response = ai_services.is_product_suitable(check.name, get_ingredients_by_product(db, check.id), get_allergens_by_client(db, client.id))
    if response.lower() == "no":
        recommendations = ai_services.get_product_recommendations(check, get_product_by_category_without_blacklisted(db, check.category_id, check.id), get_allergens_by_client(db, client.id))
        print(recommendations)
    else:
        print("Product is suitable")
    
    
    
@app.get("/get/{client_id}/shopping_cart/products")
async def get_products_in_shopping_cart(client_id: int, db: Session = Depends(get_db)):
    """Retrieve all products in the shopping cart for a given client as a streaming response."""
    shopping_cart_items = get_shopping_cart_by_client(db, client_id)
    cart_products = []
    for item in shopping_cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with ID {item.product_id} not found")
        cart_products.append({
            "product_id": product.id,
            "name": product.name,
            "brand": product.brand,
            "price": product.price,
            "quantity": item.quantity,  
            "weight": product.weight,
            "store_location": product.store_location
        })

    def iter_content():
        content = json.dumps({"client_id": client_id, "cart_products": cart_products})
        yield content  

    return StreamingResponse(iter_content(), media_type="application/json")

@app.post("/login")
async def login(db: Session = Depends(get_db), username: str = Header(...), password: str = Header(...)):
    """Login endpoint that checks if username and password match."""
    client = db.query(Client).filter(Client.name == username and Client.password==password).first()
    if not client:
        client_id = add_client(db, username, "915193363", "22222222222", "12-12-1980", password)
    else: 
        client_id = client.id
    return {client_id}

@app.post("/addToBlacklist")
async def add_allergen_to_blacklist(allergen_name: str = Body(...),  client_id: int = Header(...), db: Session = Depends(get_db)):
    """Add an allergen to a client's blacklist."""
    client = get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    allergen_id = add_allergen(db=db, client_id=client_id, name=allergen_name)
    return {"message": f"Allergen '{allergen_name}' added to blacklist successfully", "allergen_id": allergen_id}


@app.post("/pay")
async def pay(client_id: int = Header(...), db: Session = Depends(get_db)):
    """Deletes all products in shopping cart for a given client when they make a payment."""
    
    shopping_cart_items = get_shopping_cart_by_client(db, client_id)
    
    if not shopping_cart_items:
        raise HTTPException(status_code=404, detail="No products found in shopping cart for this client.")
    
    try:
        delete_shopping_cart_items(db, client_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error while deleting shopping cart items.")
    
    return {"message": "All items removed from shopping cart successfully!"}

@app.get("/takeMeThere")
async def takeMeThere(prodcut_id: int = Header(...), db: Session = Depends(get_db)):
    """Gets product location"""
    
    product = get_product(db, prodcut_id)

    if not product:
        raise HTTPException(status_code=404, detail="No product found for this product id.")
    return {"message": product.store_location}

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    client.subscribe(MQTT_TOPIC)  # Listen for messages from Arduino

def on_message(client, userdata, message):
    """Handles incoming barcodes from Arduino."""
    db = SessionLocal()  
    try:
        barcode = message.payload.decode()
        print(f"Received barcode: {barcode}")
        product = get_product_by_barcode(barcode)
        if product:
            client_id = 1  
            add_shopping_cart(db, client_id=client_id, product_id=product.id)
            print(f"Added {product.name} to shopping cart for Client {client_id}")
        else:
            print(f"Product not found for barcode {barcode}")

    except Exception as e:
        print(f"Error processing barcode: {e}")
    finally:
        db.close() 

populate_db()
example_data()
