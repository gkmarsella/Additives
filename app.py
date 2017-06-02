
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_modus import Modus
import sys
import os
import requests
import openfoodfacts

app = Flask(__name__)
api = Modus(app)


usda_key = app.config['USDA_KEY'] = os.environ.get('USDA_KEY')

@app.route('/', methods=[ "GET"])
def search():
    return render_template("search.html")


@app.route('/results', methods=["GET"])
def results():
    search_dict = {
        "q": request.args.get('search-food').lower(), 
        "sort":"n", 
        "api_key": usda_key,
        "format": "json",
    }
    search_response = requests.get("https://api.nal.usda.gov/ndb/search/", params=search_dict)
    search = search_response.json()
    return render_template("results.html", search=search)

@app.route('/prodadditives', methods=["GET"])
def prodadditives():
    search_dict = {"u": request.args.get('u'), "sid": request.args.get('sid'), "appid": "Additives", "api_key": food_essentials_key, "f": "json"}
    search = requests.get("http://api.foodessentials.com/label", params=search_dict).json()
    return jsonify(search)   



if os.environ.get('ENV') == 'production':
    debug = False
else:
    debug = True

def p(arg):
  print(arg)
  sys.stdout.flush()

# brands = openfoodfacts.facets.get_brands()


if __name__ == '__main__':
    app.run(debug=debug,port=3000)

