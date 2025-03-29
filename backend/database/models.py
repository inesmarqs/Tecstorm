import uuid

from database.database import Base
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Date, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Client(Base):
    """Client Table."""
    __tablename__ = "client"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    credit_card = Column(String, nullable=False)
    birth_date = Column(String, nullable=False)
    password = Column(String, nullable=False)
    
    allergens = relationship("Allergen", back_populates="client", cascade="all, delete-orphan")
    shopping_carts = relationship("ShoppingCart", back_populates="client", cascade="all, delete-orphan")
    recommendations = relationship("Recommendations", back_populates="client", cascade="all, delete-orphan")


class ShoppingCart(Base):
    """Shopping Cart Table."""
    __tablename__ = "shopping_cart"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("client.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id", ondelete="CASCADE"), nullable=False)
    uid = Column(String, nullable=False)
    success = Column(Boolean, nullable=False)

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
    product_id = Column(Integer, ForeignKey("product.id", ondelete="CASCADE"), nullable=False)
    product = relationship("Product", back_populates="nutricional_information")
    
class Category(Base):
    """Category Table"""
    __tablename__ = "category"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")


class Product(Base):
    """Product table."""
    __tablename__ = "product"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    bar_code = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    store_location = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id", ondelete="CASCADE"), nullable=False) #TODO check if is CASCADE
    ingredients = relationship("Ingredient", back_populates="product", cascade="all, delete-orphan")
    nutricional_information = relationship("NutricionalInformation", back_populates="product")
    category = relationship("Category", back_populates="products")
    recommendations_problem = relationship("Recommendations", foreign_keys="[Recommendations.product_id]", back_populates="product", cascade="all, delete-orphan")
    recommendations_solution = relationship("Recommendations", foreign_keys="[Recommendations.product_recommended_id]", back_populates="product_recommended", cascade="all, delete-orphan")
    

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
    
class Recommendations(Base):
    """Recommendations Table."""
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("client.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("product.id", ondelete="CASCADE"))
    product_recommended_id = Column(Integer, ForeignKey("product.id", ondelete="CASCADE")) 

    # Relações com especificação de chave estrangeira
    product = relationship("Product", foreign_keys=[product_id], back_populates="recommendations_problem")
    product_recommended = relationship("Product", foreign_keys=[product_recommended_id], back_populates="recommendations_solution")
    client = relationship("Client", back_populates="recommendations")

