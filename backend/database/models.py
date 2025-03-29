import uuid

from database import Base
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Client(Base):
    """Client Table."""
    __tablename__ = "client"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    credit_card = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    
    allergens = relationship("Allergen", back_populates="client", cascade="all, delete-orphan")

class ShoppingCart(Base):
    """Shopping Cart Table."""
    __tablename__ = "shopping_cart"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("client.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    client = relationship("Client", back_populates="shopping_carts")
    product = relationship("Product")

class NutricionalInformation(Base):
    """Nutricional Information Table"""
    __tablename__ = "nutricional_information"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    energy_kj = Column(Float, nullable=False)
    energy_kcal = Column(Float, nullable=False)
    lipids = Column(Float, nullable=False)
    saturated_lipids = Column(Float, nullable=False)
    carbon_hidrats = Column(Float, nullable=False)
    sugar_carbon_hidrats = Column(Float, nullable=False)
    fiber = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)
    salt = Column(Float, nullable=False)


class Product(Base):
    """Product table."""
    __tablename__ = "product"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    bar_code = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    nutricional_information_id = Column(Integer, ForeignKey("nutricional_information.id", ondelete="CASCADE"))
    weight = Column(Float, nullable=False)
    store_location = Column(String, nullable=False)
    nutricional_information = relationship("NutricionalInformation")
    ingredients = relationship("Ingredient", back_populates="product", cascade="all, delete-orphan")


class Ingredient(Base):
    """Ingredient Table."""
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("product.id", ondelete="CASCADE"))
    name = Column(String, nullable=False)

    product = relationship("Product", back_populates="ingredients")


class Allergen(Base):
    """Allergen Table."""
    __tablename__ = "allergens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("client.id", ondelete="CASCADE"))
    name = Column(String, nullable=False)

    client = relationship("Client", back_populates="allergens")
