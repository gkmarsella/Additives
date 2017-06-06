
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_modus import Modus
import sys
import os
import requests

app = Flask(__name__)
api = Modus(app)


usda_key = app.config['USDA_KEY'] = os.environ.get('USDA_KEY')

@app.route('/', methods=[ "GET"])
def search():
    return render_template("search.html")


@app.route('/results', methods=["GET"])
def results():

    # searching for foods
    search_dict = {
        "q": request.args.get('search-food').lower(), 
        "sort":"n", 
        "max": "10",
        "api_key": usda_key,
        "format": "json",
    }
    search_response = requests.get("https://api.nal.usda.gov/ndb/search/", params=search_dict)
    search = search_response.json()

    # grabbing all product names
    product_list = search['list']['item']

    products = []
    for i in product_list:
        products.append(i['name'])

    ndbno_list = []
    for i in product_list:
        ndbno_list.append(i['ndbno'])

    ingredients = []
    for i in ndbno_list:
        ingredients.append(ingredient_lookup(i)['report']['food']['ing']['desc'])

    # combined = list(zip(products, ingredients))

    counter = 0
    prodlength = len(products)
    product_obj = {}
    while prodlength > counter:
        for i in products:
            product_obj[i] = ingredients[counter]  
            counter = counter+1

    # list of all additives in DB
    additive_list = {}
    for i in get_additives():
        additive_list[i['name']] = i['code']

    return render_template("results.html", search=search, product_obj=product_obj, additive_list=additive_list, ingredients=ingredients)

def ingredient_lookup(ndbno):
    # getting ndbno numbers
    search_ndbno_dict = {
        "ndbno": ndbno,
        "type": "f",
        "api_key": usda_key,
        "format": "json",
    }
    search_ndbno_response = requests.get("https://api.nal.usda.gov/ndb/reports", params=search_ndbno_dict)
    search_ndbno = search_ndbno_response.json()
    return search_ndbno

def get_additives():
    response = requests.get("https://vx-e-additives.p.mashape.com/additives?locale=en&order=asc&sort=last_update",
      headers={
        "X-Mashape-Key": "xSEQIb1gTTmshMeAu6VHKTQwea6cp1vQLqsjsnv1Bgx0gMeyl6",
        "Accept": "application/json"
      }
    )

    return response.json()

def additive_function(code):
    response = requests.get("https://vx-e-additives.p.mashape.com/additives/951?locale=en",
      headers={
        "X-Mashape-Key": "xSEQIb1gTTmshMeAu6VHKTQwea6cp1vQLqsjsnv1Bgx0gMeyl6",
        "Accept": "application/json"
      }
    )

    return response.json()

def upc_lookup(upcode):
    response = requests.get("http://api.walmartlabs.com/v1/items?",
        headers={
            "apiKey": "qkwugbctetqe4t6yweybcdx9",
            "format": "json",
            "upc": upcode
        }
    )

    return response.json()

if os.environ.get('ENV') == 'production':
    debug = False
else:
    debug = True

if __name__ == '__main__':
    app.run(debug=debug,port=3000)
