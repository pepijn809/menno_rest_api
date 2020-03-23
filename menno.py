# Importeer: Flask, JSONify, Requests + Flask_PyMongo en PyMongo
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

# Naam van de Flask applicatie
app = Flask(__name__)

# Mongo Database & MongoDB Connection string
app.config['MONGO_DBNAME'] = 'menno'
app.config['MONGO_URI'] = 'mongodb+srv://pepijn:pepijn@menno-cluster-miz8h.mongodb.net/menno'

# Variabel PyMongo App
mongo = PyMongo(app)

# Flask Route - Members \ GET all documents from 'Members Collection'.
@app.route('/members', methods=['GET'])
# Function 'get_all_members'
def get_all_members():
    framework = mongo.db.members

    output = []

    for q in framework.find():
        output.append({'voornaam': q['voornaam'], 'achternaam': q['achternaam']})
    # Return the output in JSON
    return jsonify({'result': output})

# Flask Route - Members \ GET specified document based on <name> from 'Members Collection'.
@app.route('/members/<name>', methods=['GET'])
# Function 'get_one_framework'
def get_one_framework(name):
    framework = mongo.db.members

    q = framework.find_one({'voornaam': name})

    if q:
        output = {'voornaam': q['voornaam'], 'achternaam': q['achternaam']}
    else:
        output = 'Sorry. We konden geen resultaten vinden...'
    # Return the output in JSON
    return jsonify({'result': output})

# Flask Route - Members \ POST specified document based on <name> and <language> to 'Members Collection'.
@app.route('/members', methods=['POST'])
def add_framework():
    framework = mongo.db.members

    name = request.json['voornaam']
    language = request.json['achternaam']

    framework_id = framework.insert_one({'voornaam': name, 'achternaam': language})
    new_framework = framework.find_one({'_id': framework_id})

    output = {'voornaam': new_framework['voornaam'], 'achternaam': new_framework['achternaam']}
    # Return the output in JSON
    return jsonify({'result': output})

if __name__ == '__main__':
    app.run(debug=True)
