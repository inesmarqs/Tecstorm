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
    delete_shopping_cart_items
)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
    
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
            "weight": product.weight,
            "store_location": product.store_location,
            "product flagged": item.success
        })

    def iter_content():
        content = json.dumps({"client_id": client_id, "cart_products": cart_products})
        yield content  

    return StreamingResponse(iter_content(), media_type="application/json")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await connect_client(websocket,"1")
    try:
        while True:
            await websocket.receive_text()  # apenas mantém a ligação ativa
    except:
        disconnect_client(websocket)

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
async def add_allergen_to_blacklist(allergen_name: str = Body(...),  client_id: str = Header(...), db: Session = Depends(get_db)):
    """Add an allergen to a client's blacklist."""
    client_id = int(client_id)
    client = get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    allergen_id = add_allergen(db=db, client_id=client_id, name=allergen_name)
    return {"message": f"Allergen '{allergen_name}' added to blacklist successfully", "allergen_id": allergen_id}

@app.post("/deleteIngredientFromBlackList")
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

        
mqtt_thread = threading.Thread(target=start_mqtt)
mqtt_thread.start()

def test_client():
    db = next(get_db())
    Client_id = add_client(db, "test", "915193363", "22222222222", "12-12-1980", "test")
    connect_client(websocket="1",client_id=Client_id)
    alle = add_allergen(db=db, client_id=Client_id, name="frutos de casca rija")
    
test_client()