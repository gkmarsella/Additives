from factual import Factual
from flask import Flask, render_template, request, redirect, url_for
from flask_modus import Modus
import os
import pandas as pd
import requests



# Search Products












# getting data from excel sheet
table = pd.read_excel('fdaadd.xls')
 
# creating a list from data from fda excel sheet
# additive_list = []
# ad = table["FDA"]
# for add in ad:
#     additive_list.append(add)
ad = table["additive"]
additive_list = [add for add in ad]

app = Flask(__name__)
api = Modus(app)

food_essentials_key = app.config['FOOD_ESSENTIALS_KEY'] = os.environ.get('FOOD_ESSENTIALS_KEY')

key = app.config['KEY'] = os.environ.get('KEY')
secret = app.config['SECRET'] = os.environ.get('SECRET')


@app.route('/', methods=[ "GET"])
def search():
    return render_template("search.html")


# show list of food items by name
# --------------When API works -------------
# @app.route('/results', methods=["GET"])
# def results():

#     productData = products.search(request.args.get('search-food')).data()

#     list1 = [product.get('category') for product in productData]
#     categories = list(set(list1))

#     # to get ingredients 
#     for product in productData:
#         id = product['factual_id']
#         loweredIngredients = f.get_row('products-cpg-nutrition', id).get('ingredients')
#         if loweredIngredients:
#             product['ingredients'] = [x.upper() for x in loweredIngredients]


#     ad = table["additive"]
#     additive_list = [add for add in ad]

#     return render_template("results.html", products=productData, categories=categories, additive_list=additive_list)


# -------------testing for when API is down-----------
# @app.route('/results', methods=["GET"])
# def results():

#     productData = products.search(request.args.get('search-food')).data()

#     list1 = [product.get('category') for product in productData]
#     categories = list(set(list1))

#     # to get ingredients 
#     for product in productData:
#         id = product['factual_id']
#         loweredIngredients = f.get_row('products-cpg-nutrition', id).get('ingredients')
#         if loweredIngredients:
#             product['ingredients'] = [x.upper() for x in loweredIngredients]


#     ad = table["additive"]
#     additive_list = [add for add in ad]

#     return render_template("results.html", products=productData, categories=categories, additive_list=additive_list)
def get_sid():
    sid_dict = {"api_key": food_essentials_key, "f": "json", "v": "2.00"}
    sid = requests.get("http://api.foodessentials.com/createsession", params=sid_dict).json()["session_id"]
    return sid

@app.route('/results', methods=["GET"])
def results():
    # new session every time
    sid = get_sid()

    search_dict = {"q": request.args.get('search-food').lower(), "n": 100, "sid": sid, "s": 1, "f": "json", "v": "2.00", "api_key": food_essentials_key}
    search = requests.get("http://api.foodessentials.com/searchprods", params=search_dict).json()
    return render_template("results.html", search=search)


@app.route('/ingredients', methods=["GET"])
def ingredients():
    productData = products.search(request.args.get('factual_id')).data()
    return render_template("ingredients.html", product=productData)

@app.route('/index')
def index():
    return render_template("index.html", product=products) 


# getting data from api
f = Factual(key,secret)

products = f.table('products-cpg')


def get_product(val):
    inpt = products.search(val)
    id = inpt.data()[0]['factual_id']
    data = f.get_row('products-cpg-nutrition', id)
    return data

def searching(val):
    inpt = products.search(val)
    id = inpt.data()[0]['factual_id']
    data = f.get_row('products-cpg-nutrition', id)
    if (data['category']) in category_list:
        return (data['ingredients'])
    else:
        print("No products found")

def search_brand(brand):
    fix_word = brand.lower().title()
    inpt = products.search(fix_word)
    id = inpt.data()[0]['factual_id']
    data = f.get_row('products-cpg-nutrition', id)
    if (data['category']) in category_list:
        return (data)
    else:
        print("No brands found")

def search_product(val):
    return products.search(val).data()

    



category_list = ['Alcoholic Beverages', 'Baby Food', 'Baking Ingredients', 'Baking Products', 'Beans', 'Beverages', 'Bread',
                 'Breakfast Foods', 'Butters', 'Cakes', 'Candy', 'Canned Food', 'Canned Fruits & Vegetables', 'Cheeses',
                 'Chips', 'Chocolate', 'Condiments', 'Cookies', 'Cooking Oils & Sprays', 'Crackers', 
                 'Crusts, Shells, Stuffing', 'Dairy & Dairy-Substitute Products', 'Dessert Toppings', 'Dips', 'Drink Mixers',
                 'Drink Mixes', 'Eggs', 'Energy Drinks', 'Extracts, Herbs & Spices', 'Flours', 'Food', 'Food Storage', 
                 'Frozen Foods', 'Fruit Snacks', 'Fruits', 'Garlic', 'Gift Sets', 'Gourmet Food Gifts', 'Grains',
                 'Granola Bars', 'Home Brewing & Wine Making', 'Honey', 'Hot Cocoa', 'Ice Cream & Frozen Desserts',
                 'Jams & Jellies', 'Juices', 'Lentils', 'Meat Alternatives', 'Meat, Poultry, Seafood Products',
                 'Milk & Milk Substitutes', 'Noodles & Pasta', 'Nutritional Bars, Drinks, and Shakes', 'Nuts', 'Olives',
                 'Packaged Foods', 'Party Mix', 'Pastries, Desserts & Pastry Products', 'Popcorn', 'Prepared Meals',
                 'Pudding', 'Rice', 'Salad Dressings', 'Salsas', 'Sauces', 'Seasonings', 'Sexual Wellness',
                 'Smoking Cessation', 'Snacks', 'Soda', 'Soups & Stocks', 'Sugars & Sweeteners', 'Syrups',
                 'Tea & Coffee', 'Vegetables', 'Vinegars', 'Vitamins & Supplements', 'Water', 
                 'Weight Loss Products & Supplements', 'Wheat Flours & Meals', 'Yogurt'] 
#remove?: food storage, gift sets, sexual wellness, smoking cessation, vitamins & supplements, weight loss products & supplements




if __name__ == '__main__':
    app.run(debug=True,port=3000)


# <!--        <li class="food list-group-item">   
                
#                     <img class="foodimage" src="{{product['image_urls'][0]}}" alt="{{product['product_name']}}">
                
#                 <p>
#                     <a  class="foodname">{{product['product_name']}}</a>
#                 </p>            
#             </li> -->   



