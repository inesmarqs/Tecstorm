"""Create the database for shopwise-backend."""
from pathlib import Path

from database.database import Base, engine
from database.models import Client, NutricionalInformation, Product, Ingredient, Allergen, ShoppingCart

if Path("shopwise.db").exists():
    Path("shopwise.db").unlink()

Base.metadata.create_all(bind=engine)