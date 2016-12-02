from factual import Factual
from flask import Flask, render_template, request, redirect, url_for
from flask_modus import Modus
import os
import pandas as pd
import requests


# getting data from excel sheet
table = pd.read_excel('fdaadd.xls')
 

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


def get_sid():
    sid_dict = {"api_key": food_essentials_key, "f": "json", "v": "2.00"}
    sid = requests.get("http://api.foodessentials.com/createsession", params=sid_dict).json()["session_id"]
    return sid

@app.route('/results', methods=["GET"])
def results():
    # new session every time
    sid = get_sid()

    search_dict = {"q": request.args.get('search-food').lower(), "n": 5, "sid": sid, "s": 1, "f": "json", "v": "2.00", "api_key": food_essentials_key}
    search = requests.get("http://api.foodessentials.com/searchprods", params=search_dict).json()
    return render_template("results.html", search=search, sid=sid)



if os.environ.get('ENV') == 'production':
    debug = False
else:
    debug = True

if __name__ == '__main__':
    app.run(port=3000)



# prod = requests.get("http://api.foodessentials.com/label?u=" + myupc + "&sid=" + sid + "&appid=Additives&f=json&api_key=f5hrgp2evbwm3rb7d6cxp95e")


