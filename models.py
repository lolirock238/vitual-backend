# models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Category(Base):
    __tablename__ = "category"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    
    items = relationship("Item", back_populates="category")

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    category = relationship("Category", back_populates="items")
    images = relationship("ItemImage", back_populates="item", cascade="all, delete-orphan")
    outfit_items = relationship("OutfitItem", back_populates="item", cascade="all, delete-orphan")

class Outfit(Base):
    __tablename__ = "outfits"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    occasion = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    outfit_items = relationship("OutfitItem", back_populates="outfit", cascade="all, delete-orphan")

class ItemImage(Base):
    __tablename__ = "item_images"
    
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    image_url = Column(String, nullable=False)
    
    item = relationship("Item", back_populates="images")

class OutfitItem(Base):
    __tablename__ = "outfit_items"
    
    outfit_id = Column(Integer, ForeignKey("outfits.id"), primary_key=True)
    item_id = Column(Integer, ForeignKey("items.id"), primary_key=True)
    
    outfit = relationship("Outfit", back_populates="outfit_items")
    item = relationship("Item", back_populates="outfit_items")