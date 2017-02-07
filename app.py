
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_modus import Modus
import os
import requests

app = Flask(__name__)
api = Modus(app)


food_essentials_key = app.config['FOOD_ESSENTIALS_KEY'] = os.environ.get('FOOD_ESSENTIALS_KEY')

@app.route('/', methods=[ "GET"])
def search():
    return render_template("search.html")


def get_sid():
    sid_dict = {"api_key": food_essentials_key, "f": "json", "v": "2.00", "appid": "ert", "devid": "ert", "uid": "ert"}
    response = requests.get("http://api.foodessentials.com/createsession", params=sid_dict)
    sid = response.json()["session_id"]
    return sid

@app.route('/results', methods=["GET"])
def results():
    # new session every time
    sid = get_sid()

    search_dict = {"q": request.args.get('search-food').lower(), "n": 15, "sid": sid, "s": 1, "f": "json", "v": "2.00", "api_key": food_essentials_key}
    search = requests.get("http://api.foodessentials.com/searchprods", params=search_dict).json()
    return render_template("results.html", search=search, sid=sid)

@app.route('/prodadditives', methods=["GET"])
def prodadditives():
    search_dict = {"u": request.args.get('u'), "sid": request.args.get('sid'), "appid": "Additives", "api_key": food_essentials_key, "f": "json"}
    search = requests.get("http://api.foodessentials.com/label", params=search_dict).json()
    return jsonify(search)   



if os.environ.get('ENV') == 'production':
    debug = False
else:
    debug = True

if __name__ == '__main__':
    app.run(debug=debug,port=3000)

    # work on users/watch list. Don't worry so much about table
    # take nav bar extras off
    # work on style
    # add a readme to github


# prod = requests.get("http://api.foodessentials.com/label?u=" + myupc + "&sid=" + sid + "&appid=Additives&f=json&api_key=f5hrgp2evbwm3rb7d6cxp95e")


# subl $VIRTUAL_ENV/bin/postactivate

