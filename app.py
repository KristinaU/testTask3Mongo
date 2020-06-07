import pymongo
from flask import Flask, request
from flask_pymongo import PyMongo
import models

app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/mydb")

mydb = myclient["mydb"]

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
    if models.User.create_user(request.form['username'], request.form['password']):
        return 'All good', 200

    else:
        return 'Something went wrong', 400


# list of all users
@app.route('/users', methods=['GET'])
def users():
    return 'Hi we are your users', 200


if __name__ == '__main__':
    app.run()
