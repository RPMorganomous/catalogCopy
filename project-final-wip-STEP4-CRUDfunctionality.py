from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]

editedRestaurant = restaurant
restaurantToDelete = restaurant


# Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}
# items = []
editedItem = item
itemToDelete = item

# ALL JSON PAGES
@app.route('/restaurant/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id): # check PASS
    return "This page will show an entire menu as a JSON" # FROM STEP 2 - ROUTING
    # restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    # items = session.query(MenuItem).filter_by(
    #     restaurant_id=restaurant_id).all()
    # return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurant/JSON/')
def restaurantsJSON(): # check PASS
    return "This page will show all my restaurants in JSON" # FROM STEP 2 - ROUTING
    # restaurants = session.query(Restaurant).all()
    # return jsonify(restaurants=[r.serialize for r in restaurants])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id): # check PASS
    return "This page will show a menu item as a JSON" # FROM STEP 2 - ROUTING
    # menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    # return jsonify(MenuItem=menuItem.serialize)

# ALL RESTAURANTS
@app.route('/')  # PASS
@app.route('/restaurant/') # PASS
def showRestaurants(): # check PASS
    # return "This page will show all my restaurants" # FROM STEP 2 - ROUTING
    restaurants = session.query(Restaurant).all() # FROM SETP 4 - CRUD FUNCTIONALITY
    return render_template('STEP3-restaurants.html', restaurants=restaurants)

@app.route('/restaurant/<int:restaurant_id>/') # PASS
@app.route('/restaurant/<int:restaurant_id>/menu') # PASS
def restaurantMenu(restaurant_id): # similar to showMenu - PASS
    # return 'This page is the menu for restaurant %s' % restaurant_id # FROM STEP 2 - ROUTING
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one() # FROM SETP 4 - CRUD FUNCTIONALITY
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id) # FROM SETP 4 - CRUD FUNCTIONALITY
    if items == "":
        flash("You currently have no menu items.") # FROM STEP 3 - TEMPLATES AND FORMS
    return render_template(
        'STEP3-menu.html', restaurant=restaurant, items=items, restaurant_id=restaurant_id) # FROM STEP 3 - TEMPLATES AND FORMS

@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant(): # check PASS
    # return "This page will be for making a new restaurant" # FROM STEP 2 - ROUTING

    # FROM SETP 4 - CRUD FUNCTIONALITY
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('STEP3-newRestaurant.html') # FROM STEP 3 - TEMPLATES AND FORMS

@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id): # check PASS
    # return 'This page will be for editing restaurant %s' % restaurant_id # FROM STEP 2 - ROUTING

    # FROM SETP 4 - CRUD FUNCTIONALITY
    editedRestaurant = session.query(
        Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
            return redirect(url_for('showRestaurants'))
    else:
        return render_template(
            'STEP3-editRestaurant.html', restaurant=editedRestaurant) # FROM STEP 3 - TEMPLATES AND FORMS

@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id): # check PASS
    # return 'This page will be for deleting restaurant %s' % restaurant_id # FROM STEP 2 - ROUTING

    # FROM SETP 4 - CRUD FUNCTIONALITY
    restaurantToDelete = session.query(
        Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurantToDelete)
        session.commit()
        return redirect(
            url_for('showRestaurants', restaurant_id=restaurant_id))
    else:
        return render_template(
            'STEP3-deleteRestaurant.html', restaurant=restaurantToDelete) # FROM STEP 3 - TEMPLATES AND FORMS

# CREATE NEW MENU ITEM
@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id): # check PASS
    # return 'This page is for making a new menu item for restaurant %s' %restaurant_id # FROM STEP 2 - ROUTING

    # FROM SETP 4 - CRUD FUNCTIONALITY
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('STEP3-newmenuitem.html', restaurant_id=restaurant_id) # FROM STEP 3 - TEMPLATES AND FORMS


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id): # check PASS
    # return 'This page is for editing menu item %s' % menu_id # FROM STEP 2 - ROUTING

    # FROM SETP 4 - CRUD FUNCTIONALITY
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash("Menu Item has been edited")
        flash("Nice!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'STEP3-editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem) # FROM STEP 3 - TEMPLATES AND FORMS

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id): # check PASS
    # return "This page is for deleting menu item %s" % menu_id # FROM STEP 2 - ROUTING

    # FROM SETP 4 - CRUD FUNCTIONALITY
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Menu Item has been deleted")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('STEP3-deletemenuitem.html', restaurant_id=restaurant_id, item=itemToDelete) # FROM STEP 3 - TEMPLATES AND FORMS


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
