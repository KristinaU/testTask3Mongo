import pymongo
from flask import Flask, request
from flask_pymongo import PyMongo
import models

app = Flask(__name__)

def set_db():
    client = pymongo.MongoClient()
    db = client["mydb"]
    collection = db["collection"]

    admin = {'id': '0',
                        'username': 'admin',
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
    set_db()
    if models.User.create_user(request.form['username'], request.form['password']):
        return 'All good', 200

    else:
        return 'Something went wrong', 400


# list of all users
@app.route('/users', methods=['GET'])
def users():
    return 'Hi we are your users', 200


if __name__ == '__main__':
    app.set_db()
    app.run()
