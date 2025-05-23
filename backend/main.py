import asyncio
import os
import shutil
from pathlib import Path
import ai_services
from database.database import SessionLocal
from fastapi import Depends, FastAPI, File, HTTPException, Request, UploadFile, Header, Body, WebSocket
from websocket_manager import connect_client, disconnect_client
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from database.models import Client, Product, Allergen, Ingredient, NutricionalInformation
from sqlalchemy.orm import Session
import json
import time
import threading
from mqtt_server import start_mqtt
from db_session import get_db
from websocket_manager import notify_client

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
    delete_shopping_cart_items,
    delete_recommendations,
    get_recommendations_by_product_id,
)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
def calculate_cart_total(client_id: int, db: Session):
    shopping_cart_items = get_shopping_cart_by_client(db, client_id)
    if not shopping_cart_items:
        raise ValueError(f"No products found in shopping cart for client {client_id}.")
    
    total_price = 0
    product_quantity_map = {}  
    
    for item in shopping_cart_items:
        if item.product_id in product_quantity_map:
            product_quantity_map[item.product_id] += 1
        else:
            product_quantity_map[item.product_id] = 1
    
    for product_id, quantity in product_quantity_map.items():
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError(f"Product with ID {product_id} not found.")
        
        total_price += product.price * quantity  
    return total_price

def calculate_product_total(product: Product, client_id: int, db: Session):
    shopping_cart_items = get_shopping_cart_by_client(db, client_id)
    product_quantity = 0
    for item in shopping_cart_items:
        if item.product_id == product.id:
            product_quantity += 1
            
    if product_quantity == 0:
        raise ValueError(f"Product with ID {product.id} not found in shopping cart for client {client_id}.")
    
    total_price = product.price * product_quantity 
    return total_price, product_quantity


@app.get("/get/{client_id}/shopping_cart/products")
async def get_products_in_shopping_cart(client_id: int, db: Session = Depends(get_db)):
    """Retrieve all products in the shopping cart for a given client as a streaming response, 
    including the total price and individual product totals."""
    
    shopping_cart_items = get_shopping_cart_by_client(db, client_id)
    
    product_quantity_map = {}
    for item in shopping_cart_items:
        if item.product_id in product_quantity_map:
            product_quantity_map[item.product_id] += 1
        else:
            product_quantity_map[item.product_id] = 1
    
    cart_products = []
    for product_id, quantity in product_quantity_map.items():
        product = db.query(Product).filter(Product.id == product_id).first()
        #if not product:
        #    raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")
        
        product_total = product.price * quantity
        
        # Add product details to the list
        cart_products.append({
            "product_id": product.id,
            "name": product.name,
            "brand": product.brand,
            "product_flagged": shopping_cart_items[0].success,  
            "product_total": product_total,
            "product_quantity": quantity
        })
    
    total_cart_price = calculate_cart_total(client_id, db)

    response_data = {
        "client_id": client_id,
        "cart_products": cart_products,
        "total_cart_price": total_cart_price  
    }
    
    def iter_content():
        content = json.dumps(response_data)
        yield content  

    return StreamingResponse(iter_content(), media_type="application/json")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await connect_client(websocket,"1")
    try:
        while True:
            await websocket.receive_text()  # apenas mantém a ligação ativa
    except:
        disconnect_client(websocket,"1")

@app.post("/login")
async def login(db: Session = Depends(get_db), username: str = Header(...), password: str = Header(...)):
    """Login endpoint that checks if username and password match."""
    client = db.query(Client).filter(Client.name == username and Client.password==password).first()
    if not client:
        client_id = add_client(db, username, "915193363", "22222222222", "12-12-1980", password)
    else: 
        client_id = client.id
        
    return {client_id}

@app.post("/addToBlackList")
async def add_allergen_to_blacklist(allergen_name: str = Body(...),  client_id: str = Header(...), db: Session = Depends(get_db)):
    """Add an allergen to a client's blacklist."""
    client_id = int(client_id)
    allergen_id = add_allergen(db=db, client_id=client_id, name=allergen_name)
    return {"message": f"Allergen '{allergen_name}' added to blacklist successfully", "allergen_id": allergen_id}

@app.post("/removeFromBlackList")
async def delete_allergen_from_blacklist(allergen_name: str = Body(...), client_id: str = Header(...), db: Session = Depends(get_db)):  
    """Delete an allergen from a client's blacklist."""
    client_id = int(client_id)
    client = get_client(db, client_id)
    if not client: 
        raise HTTPException(status_code=404, detail="Client not found")
    allergens = get_allergens_by_client(db, client_id)
    allergen = next((a for a in allergens if a.name == allergen_name), None)
    if not allergen:
        raise HTTPException(status_code=404, detail=f"Allergen '{allergen_name}' not found in client's blacklist")
    db.delete(allergen)
    db.commit()
    return {"message": f"Allergen '{allergen_name}' removed from blacklist successfully"}


@app.post("/pay")
async def pay(client_id: int = Header(...), db: Session = Depends(get_db)):
    """Deletes all products in shopping cart for a given client when they make a payment."""
    
    shopping_cart_items = get_shopping_cart_by_client(db, client_id)
    
    if not shopping_cart_items:
        raise HTTPException(status_code=404, detail="No products found in shopping cart for this client.")
    
    try:
        delete_shopping_cart_items(db, client_id)
        delete_recommendations(db, client_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error while deleting shopping cart items.")
    
    return {"message": "All items removed from shopping cart successfully!"}

@app.get("/takeMeThere")
async def takeMeThere(prodcut_id: str = Header(...), db: Session = Depends(get_db)):
    """Gets product location"""
    product = get_product(db, int(prodcut_id))

    if not product:
        raise HTTPException(status_code=404, detail="No product found for this product id.")
    return {"message": product.store_location}

@app.get("/getBlackList")
async def getBlackList(client_id: str = Header(...), db: Session = Depends(get_db)):
    """Gets the client's blacklist of allergens."""
    allergens = get_allergens_by_client(db, int(client_id))
    allergens_list = [allergen.name for allergen in allergens]
    return {"blacklist": allergens_list}

@app.get("/recommendations")
async def get_recommendations_for_product_and_client(
    product_id: str = Header(...), client_id: str = Header(...), db: Session = Depends(get_db)
):
    """
    Get product recommendations for a given product and client ID.
    The recommendations will take into account the client's allergens and preferences.
    """
    
    recommendation = get_recommendations_by_product_id(db,int(product_id), int(client_id))
    product = get_product(db, recommendation.product_recommended_id)
    if not product:
        raise HTTPException(status_code=404, detail="No product found for this recommendation.")
    rec_list = []
    if product:
        rec_list.append(product.name)
        rec_list.append(product.brand)
        rec_list.append(product.price)
        rec_list.append(product.store_location)
    
    print(rec_list)
    return {"response": rec_list}


mqtt_thread = threading.Thread(target=start_mqtt)
mqtt_thread.start()
