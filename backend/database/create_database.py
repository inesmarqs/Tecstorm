"""Create the database for shopwise-backend."""
from pathlib import Path

from database import Base, engine
from models import Client, NutricionalInformation, Product, Ingredient, Allergen

if Path("shopwise.db").exists():
    Path("shopwise.db").unlink()

Base.metadata.create_all(bind=engine)