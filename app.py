from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_modus import Modus
from flask_login import LoginManager
import sys
import os
import requests
import urllib.request
import json
# for logging in
from flask_login import LoginManager
# from project import db, bcrypt
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from flask_bcrypt import Bcrypt
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
api = Modus(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)


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

    try:
        search_response = requests.get("https://api.nal.usda.gov/ndb/search/", params=search_dict)
        search = search_response.json()
        product_list = search['list']['item']
    except (json.decoder.JSONDecodeError, KeyError) as e:
        no_results = request.args.get('search-food').lower()
        return render_template("400.html", no_results=no_results)


    # grabbing all product names


    products = []
    for i in product_list:
        products.append(i['name'])

    # counter for product_obj
    prodlength = len(products)

    ndbno_list = []
    for i in product_list:
        ndbno_list.append(i['ndbno'])

    ingredients = []
    for i in ndbno_list:
        try:
            ingredients.append(ingredient_lookup(i)['report']['food']['ing']['desc'])
        except (json.decoder.JSONDecodeError, KeyError) as e:
            ingredients.append("No ingredients found")

    # combined = list(zip(products, ingredients))

    
    counter = 0
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


# #############################################################
#                       LOGIN
# #############################################################
class UserForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')

from flask_login import LoginManager

# initialize the login_manager
login_manager = LoginManager()

# pass your app into the login_manager instance
login_manager.init_app(app)

# You also need to tell flask_login where it should redirect 
# someone to if they try to access a private route.
login_manager.login_view = "users.login"

# You can also change the default message when someone 
# gets redirected to the login page. The default message is
# "Please log in to access this page."
login_manager.login_message = "Please log in!"

# write a method with the user_loader decorator so that flask_login can find a current_user 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/signup', methods =["GET", "POST"])
def signup():
    form = UserForm(request.form)
    if form.validate_on_submit():
        try:
            new_user = User(form.data['username'], form.data['password'])
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError as e:
            return render_template('signup.html', form=form)
        return redirect(url_for('users.login'))
    return render_template('signup.html', form=form)


@app.route('/login', methods = ["GET", "POST"])
def login():
    form = UserForm(request.form)
    if form.validate_on_submit():
        found_user = User.query.filter_by(username = form.data['username']).first()
        if found_user:
            authenticated_user = bcrypt.check_password_hash(found_user.password, form.data['password'])
            if authenticated_user:
                return redirect(url_for('users.welcome'))
    return render_template('login.html', form=form)

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')
    

if os.environ.get('ENV') == 'production':
    debug = False
else:
    debug = True

if __name__ == '__main__':
    app.run(debug=debug,port=3000)
