# Requirements
# - Flask, JSONify, Requests, DNSPython, Flask_PyMongo, Flask_HTTPAuth, Werkzeug.Security
from flask import Flask, jsonify, request, make_response
from flask_pymongo import PyMongo
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

# Flask applicatie met HTTPAuth
app = Flask(__name__)
auth = HTTPBasicAuth()

# Geauthenticeerde gebruikers voor API
auth_users = {
    "mike": generate_password_hash("mike"),
    "pepijn": generate_password_hash("pepijn")
}

# MongoDB Instellingen
app.config['MONGO_DBNAME'] = 'menno' # MongoDB naam
app.config['MONGO_URI'] = 'mongodb+srv://pepijn:pepijn@menno-cluster-miz8h.mongodb.net/menno' # MongoDB bij MongoDB Atlas op AWS
#app.config['MONGO_URI'] = 'mongodb://mongo0.mikevdbrink.nl:27017,mongo1.mikevdbrink.nl:27017,mongo2.mikevdbrink.nl:27017/menno?replicaSet=cloud' # MongoDB Bij Google Cloud Platform (GPC)
mongo = PyMongo(app) # Variabel voor PyMongo

# Authenticatie functie - HTTPAuth op basis van 'auth_users' lijst
@auth.verify_password
def verify_password(username, password):
    if username in auth_users:
        return check_password_hash(auth_users.get(username), password)
    return False

# / route - API Homepagina
@app.route('/')
@auth.login_required
def index():
    return "Hoi, %s!" % auth.username()

# Flask Route - Users \ GET all documents from 'Users Collection'.
@app.route('/users', methods=['GET'])
@auth.login_required # Require Basic HTTPAuth
# Function 'get_all_users' - Vraag alle gebruikers op
def get_all_users():
    framework = mongo.db.users

    output = []

    for q in framework.find():
        output.append({'voornaam': q['voornaam'], 'achternaam': q['achternaam'], 'name': q['name'], 'plaats': q['plaats'], 'provincie': q['provincie'], 'adres': q['adres']})
    # Return the output in JSON
    return jsonify({'result': output})

# Flask Route - Users \ GET een specifiek document gebasseerd op de voornaam van een gebruiker in de 'Users Collectie'.
@app.route('/users/<voornaam>', methods=['GET'])
@auth.login_required # Require Basic HTTPAuth
# Function 'get_one_user' - Vraag gegevens van 1 gebruiker op op basis van voornaam
def get_one_user(voornaam):
    users = mongo.db.users

    q = users.find_one({'voornaam': voornaam})

    if q:
        output = {'voornaam': q['voornaam'], 'achternaam': q['achternaam'], 'name': q['name'], 'plaats': q['plaats'], 'provincie': q['provincie'], 'adres': q['adres']}
    else:
        output = 'Sorry! We konden geen gebruikers vinden.'
    # Return the output in JSON
    return jsonify({'result': output})

# Flask Route - Users \ POST een specifiek document gebasseerd op gebruikersdetails naar de 'Users Collectie'.
@app.route('/users', methods=['POST'])
@auth.login_required # Require Basic HTTPAuth
# Function 'add_user' - Voeg een gebruiker toe op basis van JSON data
def add_user():
    users = mongo.db.users

    voornaam = request.json['voornaam']
    achternaam = request.json['achternaam']

    users_id = users.insert_one({'voornaam': voornaam, 'achternaam': achternaam})
    new_users = users.find_one({'_id': users_id})

    output = {'voornaam': new_users['voornaam'], 'achternaam': new_users['achternaam']}
    # Return the output in JSON
    return jsonify({'result': output})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
