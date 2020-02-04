from flask import Flask, render_template, request, redirect, url_for
from database_setup import Restaurant, MenuItem, engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)


DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/')
def restaurants():
    restaurants_db = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants_db)


@app.route('/restaurants/<string:restaurant_name>/menu')
def menu(restaurant_name):
    restaurant = session.query(Restaurant).filter_by(name=restaurant_name).one()
    menu_items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, menu_items=menu_items)


# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<string:restaurant_name>/new_item', methods=['GET', 'POST'])
def new_menu_item(restaurant_name):
    if request.method == 'POST':
        restaurant = session.query(Restaurant).filter_by(name=restaurant_name).one()
        new_item = MenuItem(name= request.form['name'], restaurant_id=restaurant.id)
        session.add(new_item)
        session.commit()
        return redirect(url_for('menu', restaurant_name=restaurant.name))
    else:
        return render_template('new_menu_item.html', restaurant_name=restaurant_name)


# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<string:restaurant_name>/edit_item/<string:item_name>', methods=['GET', 'POST'])
def edit_menu_item(restaurant_name, item_name):
    if request.method == 'POST':
        restaurant = session.query(Restaurant).filter_by(name=restaurant_name).one()
        item = session.query(MenuItem).filter_by(name=item_name, restaurant_id=restaurant.id).one()
        item.name = request.form['name']
        session.add(item)
        session.commit()
        return redirect(url_for('menu', restaurant_name=restaurant.name))
    else:
        return render_template('edit_menu_item.html', restaurant_name=restaurant_name, item_name=item_name)


# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<string:restaurant_name>/delete_item/<string:item_name>', methods=['GET', 'POST'])
def delete_menu_item(restaurant_name, item_name):
    if request.method == 'POST':
        restaurant = session.query(Restaurant).filter_by(name=restaurant_name).one()
        item = session.query(MenuItem).filter_by(name=item_name, restaurant_id=restaurant.id).one()
        session.delete(item)
        session.commit()
        return redirect(url_for('menu', restaurant_name=restaurant.name))
    else:
        return render_template('delete_menu_item.html', restaurant_name=restaurant_name, item_name=item_name)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
