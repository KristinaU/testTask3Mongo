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


# Show blank index page just in case
@app.route('/')
def index():
    return 'Index Page'
#   maybe an error if http server not configured


# Show hello page to present app working
@app.route('/hello')
def hello_world():
    return 'Hello World!'


# registration
@app.route('/registration', methods=['POST'])
def registration():
    user = models.User.create_user(request.form['username'], request.form['password'])
    collection.insert(user)
#   add errors handler
    return 'User register success!', 200


# list of all users
@app.route('/users', methods=['GET'])
def users():
    result = 'So we got the users as: ' + (str(collection.distinct('username')))
#   add error handler
    return result, 200


# login functionality
@app.route('/login', methods=['POST'])
def login():
# define what time is now
    start_time = datetime.now()

# set what time token expires
    expiry_time = datetime.now() + timedelta(minutes=+30)

# an alphabet used to create random alphanumerical token
    letters = 'abcdefghyjklmnopqrstuvwxyz1234567890'

# check (in separate method) that username and password match
    if check_user(request.form['username'], request.form['password']):

# create random alphanumerical token
        token = ''.join(random.choice(letters) for i in range(32))

# set token and its expiry time to the user field in the database
        collection.update(

        { 'username': request.form['username']},

        { "$set":    { 'token': token, 'token_exp': expiry_time } }

        )

        return token, 200

    else:

# if check_user fails
        return 'Sorry, the password is wrong', 400


def check_user(username, password):
    currentpass = collection.find_one({'username': username})['password']
#   here return an error if username not found
    if (currentpass == password):
        return True
    else:
        return False


if __name__ == '__main__':
    app.run()
