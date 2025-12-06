from models import  Category, Item
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///vitual-organizer.db")
Session = sessionmaker(bind=engine)
session = Session()

# Add a category
category = Category(name="Shirts")
session.add(category)
session.commit()

# Add an item
item = Item(name="Blue Shirt", category_id=category.id)
session.add(item)
session.commit()

# Query items
for i in session.query(Item).all():
    print(i.name, i.category_id)


