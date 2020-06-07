import json
from datetime import datetime, timedelta
import random

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
    result = 'So we got the users as: ' + (str(collection.distinct('username')))
    return result, 200


# login functionality
@app.route('/login', methods=['POST'])
def login():
    start_time = datetime.now()

    expire_time = datetime.now() + timedelta(minutes=+30)

    letters = 'abcdefghyjklmnopqrstuvwxyz1234567890'

    if check_user(request.form['username'], request.form['password']):
        print('Now is ' + str(start_time))
        print('Token expires at ' + str(expire_time))
        return ''.join(random.choice(letters) for i in range(32))
    else:
        return 400


def check_user(username, password):
    if username is not None and password is not None:
        return True, 200
    else:
        return False, 400


if __name__ == '__main__':
    app.run()
