from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Database config file where the DB classes were written
from database_setup import Base, Restaurant, MenuItem

# Here we set which database engine we want to communicate with
engine = create_engine('sqlite:///restaurantmenu.db')
# Then we bind the engine with the Base class connecting the class definitions with the corresponding tables in our database
Base.metadata.bind = engine

# Next a session maker object creates a link of communication between the code execution and the engine we just created
DBSession = sessionmaker(bind=engine)
session = DBSession() 
# A session allows us to write all the operations we want to affect our database and only execute them once we call commit()
myFirstRestaurant = Restaurant(name="Pizza Palace")
session.add(myFirstRestaurant)
session.commit()

# This will send a request for all the entries in the Restaurant table from the database
session.query(Restaurant).all() 

cheesepizza = MenuItem(name="Cheese Pizza", description="Made wiith all natural ingredients and fresh mozzarella", course="Entree", price="$8.99", restaurant=myFirstRestaurant)
session.add(cheesepizza)
session.commit()

# Comprehensive query
session.query(MenuItem).all()

# Querying one entry
firstResult = session.query(Restaurant).first()
print(firstResult.name)

# Reading each entry from a table
items = session.query(MenuItem).all()
for item in items:
    print(item.name)

# Filtering each entry from a table by their name
veggie_burguers = session.query(MenuItem).filter_by(name='Veggie Burger')
for veggie_burguer in veggie_burguers:
    print(veggie_burguer.id)
    print(veggie_burguer.price)
    print(veggie_burguer.restaurant.name)
    print()

# Updating an item:
# 1) Finding the item based on its id
urban_veggie_burguer = session.query(MenuItem).filter_by(id=8).one()
print(urban_veggie_burguer.price)
# 2) Updating it
urban_veggie_burguer.price = '$2.99'
# 3) Adding it to the session
session.add(urban_veggie_burguer)
# 4) Committing the session
session.commit()

# Verifying changes
veggie_burguers = session.query(MenuItem).filter_by(name='Veggie Burger')
for veggie_burguer in veggie_burguers:
    print(veggie_burguer.id)
    print(veggie_burguer.price)
    print(veggie_burguer.restaurant.name)
    print()

# Updating many items
veggie_burguers = session.query(MenuItem).filter_by(name='Veggie Burger')
for veggie_burguer in veggie_burguers:
    if veggie_burguer.price != '$2.99':
        veggie_burguer.price = '$2.99'
        session.add(veggie_burguer)
        session.commit()

# Verifying the changes
veggie_burguers = session.query(MenuItem).filter_by(name='Veggie Burger')
for veggie_burguer in veggie_burguers:
    print(veggie_burguer.id)
    print(veggie_burguer.price)
    print(veggie_burguer.restaurant.name)
    print()

# Deleting an item:
# 1) Finding the item based on its name
spinach = session.query(MenuItem).filter_by(name='Spinach Ice Cream').one()
print(spinach.restaurant.name)
# 2) Deleting item
session.delete(spinach)
# 3) Comitting the session
session.commit()