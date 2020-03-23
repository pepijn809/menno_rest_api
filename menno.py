# Importeer: Flask, JSONify, Requests, DNSpython + Flask_PyMongo en PyMongo
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

# Naam van de Flask applicatie
app = Flask(__name__)

# Mongo Database & MongoDB Connection string
app.config['MONGO_DBNAME'] = 'menno'
app.config['MONGO_URI'] = 'mongodb+srv://pepijn:pepijn@menno-cluster-miz8h.mongodb.net/menno'

# Variabel PyMongo App
mongo = PyMongo(app)

# Flask Route - Users \ GET all documents from 'Users Collection'.
@app.route('/users', methods=['GET'])
# Function 'get_all_users' - Vraag alle gebruikers op
def get_all_users():
    framework = mongo.db.users

    output = []

    for q in framework.find():
        output.append({'voornaam': q['voornaam'], 'achternaam': q['achternaam']})
    # Return the output in JSON
    return jsonify({'result': output})

# Flask Route - Users \ GET specified document based on <name> from 'Users Collection'.
@app.route('/users/<name>', methods=['GET'])
# Function 'get_one_user' - Vraag gegevens van 1 gebruiker op
def get_one_user(name):
    users = mongo.db.users

    q = users.find_one({'voornaam': name})

    if q:
        output = {'voornaam': q['voornaam'], 'achternaam': q['achternaam']}
    else:
        output = 'Sorry! We konden geen gebruikers vinden.'
    # Return the output in JSON
    return jsonify({'result': output})

# Flask Route - Users \ POST specified document based on <name> and <language> to 'Users Collection'.
@app.route('/users', methods=['POST'])
# Function 'add_user' - Voeg een gebruiker toe op basis van JSON
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
    app.run(debug=True)
