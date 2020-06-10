import json
from datetime import datetime, timedelta
import random
import pymongo
from flask import Flask, request
import models

app = Flask(__name__)

client = pymongo.MongoClient()
db = client["mydb"]
collection = db["collection"]
item_counter = db["item_counter"]
db.item_counter.insert({'count': 0})
items_collection = db["items_collection"]


# Show blank index page just in case
@app.route('/')
def index():
    return "Index Page"


# Show hello page to present app working
@app.route('/hello')
def hello_world():
    return "Hello World!"


# registration
@app.route('/registration', methods=['POST'])
def registration():
    try:
        this_username = request.get_json()['username']
        this_password = request.get_json()['password']
    except KeyError:
        return json.dumps("Either Username or Password missing"), 500
    except:
        return json.dumps("Query content is not valid JSON"), 400

    if this_username == "" or this_password == "":
        # this line does not return the message but works well
        return json.dumps("Please fill required fields"), 204

    elif user_exists(this_username):
        return json.dumps("Username already registered!"), 400

    else:
        user = models.User.create_user(
            this_username,
            this_password
        )
        try:
            collection.insert(user)
        except:
            return json.dumps("Database server error"), 500

        return json.dumps("User register success!"), 200


def user_exists(username):
    if collection.find_one({'username': username}) is not None:
        return True
    else:
        return False


# list of all users
@app.route('/users', methods=['GET'])
def users():
    try:
        result = collection.distinct('username')
    except:
        return json.dumps("Database server error"), 500
    return json.dumps(result, indent=4), 200


# login functionality
@app.route('/login', methods=['POST'])
def login():
    # define what time is now
    start_time = datetime.now()

    # set what time token expires
    expiry_time = datetime.now() + timedelta(minutes=+30)

    # Here we may check database and remove expired tokens
    # that is not implemented as beyond the task specification

    # an alphabet used to create random alphanumerical token
    letters = 'abcdefghyjklmnopqrstuvwxyz1234567890'

    try:
        this_username = request.get_json()['username']
        this_password = request.get_json()['password']
    except:
        return "Query content is not valid JSON", 400

    # check (in separate method) that username and password match
    if check_user(this_username, this_password):

        # create random alphanumerical token
        token = ''.join(random.choice(letters) for i in range(32))

        # set token and its expiry time to the user field in the database
        try:
            collection.update(
                {'username': this_username},
                {"$set": {'token': token, 'token_exp': expiry_time}}
            )
            return json.dumps(token), 200
        except:
            return json.dumps("Database server error"), 500
    else:
        # if check_user fails
        return "Username and password do not match", 400


def check_user(username, password):
    try:
        currentpass = collection.find_one({'username': username})['password']
    except:
        return False
    return currentpass == password


# this method ensures the items have unique (int) id
def get_count():
    return item_counter.find_and_modify(update={'$inc': {'count': 1}},
                                        new=True).get('count')


# add item
@app.route('/items/new', methods=['POST'])
def add_item():
    try:
        item_holder_username = collection.find_one(
            {'token': request.get_json()['token']})['username']
    except:
        return json.dumps(
            "Your token is not valid or has been expired"
        ), 500

    item = models.Item.create_item(
        get_count(),
        item_holder_username, request.get_json()['item_name']
    )
    try:
        items_collection.insert(item)
    except:
        return json.dumps("Database server error"), 500

    result = str(item)
    return json.dumps("Item added! Its attributes are: " + result), 200


# get items for user identified by token
@app.route('/items', methods=['GET'])
def items():
    try:
        token = request.args['token']
    except:
        return "Sorry, request failed", 400
    try:
        current_username = collection.find_one({'token': token})['username']
    except:
        return json.dumps(
            "Your token is not valid or has been expired"
        ), 500

    items = list(items_collection.find(
        {'username': current_username},
        {'_id': 0})
    )

    return json.dumps(items, indent=4)


# delete item
@app.route('/items/<item_id_str>', methods=['DELETE'])
def delete_item(item_id_str):
    try:
        token = request.args['token']
    except:
        return json.dumps("Sorry, request failed"), 400
    # here url id argument requires conversion to int to become valid field argument
    try:
        item_id = int(item_id_str)
    except ValueError:
        return json.dumps("Could not convert Item ID to an integer.")

    if check_item(token, item_id):
        item = items_collection.find_one({'id': item_id})
        items_collection.remove(item)
# this line does not return the message but works well
        return json.dumps("Item successfully deleted"), 204
    else:
# this result will show if either token or id invalid
        return json.dumps("Data you provided do not match our records"), 400


# This method checks if token provided and item to delete
# belong to the same user
def check_item(token, item_id):
    try:
        username_token_holder = collection.find_one(
            {'token': token})['username']
        username_item_holder = items_collection.find_one(
            {'id': item_id})['username']
# if 'username' fields do not match we raise an error regardless reason
    except:
        return False
    if username_token_holder is not None:
        return username_token_holder == username_item_holder
    else:
        return False


if __name__ == '__main__':
    app.run()
