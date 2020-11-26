from flask import Flask, request, json, jsonify, Response
from flask_pymongo import PyMongo, ObjectId
from bson import json_util
from flask_cors import CORS

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost/schedule"
mongo = PyMongo(app)
cors = CORS(app)

db = mongo.db.user


@app.route('/create', methods=['POST'])
def create(): 
    id = db.insert({
        'name': request.json['name'],
        'lastname': request.json['lastname'],
        'document': request.json['document'],
        'birthdate': request.json['birthdate'],
        'city': request.json['city'],
        'neighborhood': request.json['neighborhood'],
        'cellphone': request.json['cellphone']
    })
    return jsonify(str(ObjectId(id)))

@app.route('/list', methods=['GET'])
def list():
    user = []
    for doc in db.find():
        user.append({
            '_id': str(ObjectId(doc['_id'])),
            'name': doc['name'],
            'lastname': doc['lastname'],
            'document': doc['document'],
            'birthdate': doc['birthdate'],
            'city': doc['city'],
            'neighborhood': doc['neighborhood'],
            'cellphone': doc['cellphone']
        })
    return jsonify(user)    

@app.route('/user/<id>', methods=['GET'])
def getUser(id):
    user = db.find_one({'_id': ObjectId(id)})
    print(user)
    return jsonify({
        '_id': str(ObjectId(user['_id'])),
        'name': user['name'],
        'lastname': user['lastname'],
        'document': user['document'],
        'birthdate': user['birthdate'],
        'city': user['city'],
        'neighborhood': user['neighborhood'],
        'cellphone': user['cellphone']
    })

@app.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    db.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': 'User deleted '})
    
@app.route('/update/<id>', methods=['PUT'])
def update(id):
    db.update_one({'_id': ObjectId(id)}, {'$set':{
        'name': request.json['name'],
        'lastname': request.json['lastname'],
        'document': request.json['document'],
        'birthdate': request.json['birthdate'],
        'city': request.json['city'],
        'neighborhood': request.json['neighborhood'],
        'cellphone': request.json['cellphone']
    }})
    return jsonify({'msg': 'User Update'})
    
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)