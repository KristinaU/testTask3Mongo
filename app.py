import json

import pymongo
from flask import Flask, request
from flask_pymongo import PyMongo
import models
from bson.objectid import ObjectId

app = Flask(__name__)

client = pymongo.MongoClient()
db = client["mydb"]
collection = db["collection"]

admin = {'username': 'admin',
         'password': 'password1',
         'token': None,
         'token_exp': None}
collection.insert(admin)
print ('Oh we have an admin')



# Show blank index page just in case
@app.route('/')
def index():
    return 'Index Page'


# Show hello page to present app working
@app.route('/hello')
def hello_world():
    return 'Hello World!'


# registration
@app.route('/registration', methods=['POST'])
def registration():
    user = models.User.create_user(request.form['username'], request.form['password'])
    collection.insert(user)
    return 'Ok', 200


# list of all users
@app.route('/users', methods=['GET'])
def users():
    result = 'Here are the users: ' + (str(collection.distinct('username')))
    return result, 200


if __name__ == '__main__':
    app.run()
