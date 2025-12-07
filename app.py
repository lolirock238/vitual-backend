# app.py
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models import Category, Item, Outfit, ItemImage, OutfitItem
import os
import shutil
import json

# Initialize DB tables
init_db()

app = FastAPI()

# =========================
# STATIC FILES
# =========================
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# =========================
# DATABASE SESSION
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# CATEGORY ENDPOINTS
# =========================
@app.post("/categories/")
def create_category(name: str = Form(...), db: Session = Depends(get_db)):
    category = Category(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@app.get("/categories/")
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

# =========================
# ITEM ENDPOINTS
# =========================
@app.post("/items/")
def create_item(
    category_id: int = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validate category exists
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Save item
    item = Item(category_id=category_id)
    db.add(item)
    db.commit()
    db.refresh(item)

    # Save image to uploads folder
    filename = f"{item.id}_{image.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # Save image record
    item_image = ItemImage(item_id=item.id, image_url=f"/uploads/{filename}")
    db.add(item_image)
    db.commit()
    db.refresh(item_image)

    return {"id": item.id, "category_id": item.category_id, "image_url": item_image.image_url}

@app.get("/items/")
def get_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    results = []
    for item in items:
        image = db.query(ItemImage).filter(ItemImage.item_id == item.id).first()
        results.append({
            "id": item.id,
            "category_id": item.category_id,
            "image_url": image.image_url if image else None
        })
    return results

# =========================
# OUTFIT ENDPOINTS
# =========================
@app.post("/outfits/")
def create_outfit(
    name: str = Form(...),
    items: str = Form(...),  # JSON list of item IDs
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    # Save outfit image if provided
    image_url = None
    if image:
        filename = f"outfit_{image.filename}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = f"/uploads/{filename}"

    # Create outfit
    outfit = Outfit(name=name, image_url=image_url)
    db.add(outfit)
    db.commit()
    db.refresh(outfit)

    # Associate items
    try:
        item_ids = json.loads(items)
        if not isinstance(item_ids, list):
            raise ValueError
    except(json.JSONDecodeError, ValueError):
        raise HTTPException(status_code=400, detail="Items must be a valid JSON list of item IDs")

    for item_id in item_ids:
        db_item = db.query(Item).filter(Item.id == item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
        outfit_item = OutfitItem(outfit_id=outfit.id, item_id=item_id)
        db.add(outfit_item)

    db.commit()

    return {
        "id": outfit.id,
        "name": outfit.name,
        "image_url": outfit.image_url,
        "items": item_ids
    }

@app.get("/outfits/")
def get_outfits(db: Session = Depends(get_db)):
    outfits = db.query(Outfit).all()
    results = []
    for outfit in outfits:
        items = db.query(OutfitItem).filter(OutfitItem.outfit_id == outfit.id).all()
        results.append({
            "id": outfit.id,
            "name": outfit.name,
            "image_url": outfit.image_url,
            "items": [i.item_id for i in items]
        })
    return results
