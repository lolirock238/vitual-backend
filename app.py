# app.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Category, Item, Outfit, ItemImage, OutfitItem
from database import SessionLocal, init_db

# Initialize DB tables
init_db()

app = FastAPI()

# Root endpoint (add this)
@app.get("/")
def read_root():
    return {"message": "Welcome to Virtual Organizer API"}


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#CREATING ENDPOINTS.
#Endpoint for category
# Create a category
@app.post("/categories/")
def create_category(name: str, db: Session = Depends(get_db)):
    category = Category(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

# Get all categories
@app.get("/categories/")
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

# Update a category
@app.put("/categories/{category_id}")
def update_category(category_id: int, name: str, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category.name = name
    db.commit()
    db.refresh(category)
    return category

# Delete a category
@app.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"message": "Category deleted"}




#Endpoint for item
# Create an item
@app.post("/items/")
def create_item(name: str, category_id: int, db: Session = Depends(get_db)):
    item = Item(name=name, category_id=category_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# Get all items
@app.get("/items/")
def get_items(db: Session = Depends(get_db)):
    return db.query(Item).all()

# Update an item
@app.put("/items/{item_id}")
def update_item(item_id: int, name: str = None, category_id: int = None, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if name:
        item.name = name
    if category_id:
        item.category_id = category_id
    db.commit()
    db.refresh(item)
    return item

# Delete an item
@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item deleted"}


#Endpoint for oufit
#create an outfit
@app.post("/outfits/")
def create_outfit(name: str, occasion: str = None, db: Session = Depends(get_db)):
    outfit = Outfit(name=name, occasion=occasion)
    db.add(outfit)
    db.commit()
    db.refresh(outfit)
    return outfit
#Get all oufits
@app.get("/outfits/")
def get_outfits(db: Session = Depends(get_db)):
    return db.query(Outfit).all()
#update an oufit
@app.put("/outfits/{outfit_id}")
def update_outfit(outfit_id: int, name: str = None, occasion: str = None, db: Session = Depends(get_db)):
    outfit = db.query(Outfit).filter(Outfit.id == outfit_id).first()
    if not outfit:
        raise HTTPException(status_code=404, detail="Outfit not found")
    if name:
        outfit.name = name
    if occasion:
        outfit.occasion = occasion
    db.commit()
    db.refresh(outfit)
    return outfit
#delete an outfit
@app.delete("/outfits/{outfit_id}")
def delete_outfit(outfit_id: int, db: Session = Depends(get_db)):
    outfit = db.query(Outfit).filter(Outfit.id == outfit_id).first()
    if not outfit:
        raise HTTPException(status_code=404, detail="Outfit not found")
    db.delete(outfit)
    db.commit()
    return {"message": "Outfit deleted"}

#Endpoint for item image and oufit item
# ItemImage
@app.post("/item_images/")
def add_item_image(item_id: int, image_url: str, db: Session = Depends(get_db)):
    image = ItemImage(item_id=item_id, image_url=image_url)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image

@app.get("/item_images/")
def get_item_images(db: Session = Depends(get_db)):
    return db.query(ItemImage).all()

# OutfitItem (associate item with outfit)
@app.post("/outfit_items/")
def add_item_to_outfit(outfit_id: int, item_id: int, db: Session = Depends(get_db)):
    association = OutfitItem(outfit_id=outfit_id, item_id=item_id)
    db.add(association)
    db.commit()
    db.refresh(association)
    return association

@app.get("/outfit_items/")
def get_outfit_items(db: Session = Depends(get_db)):
    return db.query(OutfitItem).all()
