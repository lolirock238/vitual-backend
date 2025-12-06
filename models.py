from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    
    items = relationship("Item", back_populates="category")

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    category = relationship("Category", back_populates="items")
    images = relationship("ItemImage", back_populates="item")
    outfits = relationship("OutfitItem", back_populates="item")

class Outfit(Base):
    __tablename__ = "outfits"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    occasion = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    items = relationship("OutfitItem", back_populates="outfit")

class ItemImage(Base):
    __tablename__ = "item_images"
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    image_url = Column(Text, nullable=False)
    
    item = relationship("Item", back_populates="images")

class OutfitItem(Base):
    __tablename__ = "outfit_items"
    outfit_id = Column(Integer, ForeignKey("outfits.id"), primary_key=True)
    item_id = Column(Integer, ForeignKey("items.id"), primary_key=True)
    
    outfit = relationship("Outfit", back_populates="items")
    item = relationship("Item", back_populates="outfits")
