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
    return 'Index Page'


#   maybe an error if http server not configured


# Show hello page to present app working
@app.route('/hello')
def hello_world():
    return json.dumps('Hello World!')


# registration
@app.route('/registration', methods=['POST'])
def registration():

    this_username = request.get_json()['username']
    this_password = request.get_json()['password']
    if user_exists(this_username):
        return json.dumps('Username already registered!'), 400
    else:
        user = models.User.create_user(
            this_username,
            this_password
        )
        collection.insert(user)

        return json.dumps('User register success!'), 200

def user_exists(username):
    if collection.find_one({'username': username}) is not None:
        return True
    else:
        return False



# list of all users
@app.route('/users', methods=['GET'])
def users():
    result = collection.distinct('username')
    #   add error handler
    return json.dumps(result, indent=4), 200


# login functionality
@app.route('/login', methods=['POST'])
def login():
    # define what time is now
    start_time = datetime.now()

    # set what time token expires
    expiry_time = datetime.now() + timedelta(minutes=+30)

    # an alphabet used to create random alphanumerical token
    letters = 'abcdefghyjklmnopqrstuvwxyz1234567890'

#    try:

#        request = r.json()
#        return 'All good', 200
#    except ValueError:
#        return 'Query content is not valid JSON', 400

    this_username = request.get_json()['username']
    this_password = request.get_json()['password']

    # check (in separate method) that username and password match
    if check_user(this_username, this_password):

        # create random alphanumerical token
        token = ''.join(random.choice(letters) for i in range(32))

        # set token and its expiry time to the user field in the database
        collection.update(
            {'username': this_username},
            {"$set": {'token': token, 'token_exp': expiry_time}}
        )
        return json.dumps(token), 200

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


def getCount(item_counter):
   return item_counter.find_and_modify( update= { '$inc': {'count': 1}},
                                        new=True ).get('count')


# add item
@app.route('/items/new', methods=['POST'])
def add_item():
    item_holder_username = collection.find_one(
        {'token': request.get_json()['token']})['username']
    item = models.Item.create_item(
          getCount(db.item_counter),
          item_holder_username, request.get_json()['item_name']
    )
    items_collection.insert(item)
    #   add errors handler
    result = str(item)
    return json.dumps('Item added! Its attributes are: ' + result), 200


# get items
@app.route('/items', methods=['GET'])
def items():
    token = request.args['token']
    current_username = collection.find_one({'token': token})['username']
    items = list(items_collection.find(
        {'username': current_username},
        {'_id': 0})
    )
    #   add error handler
    return json.dumps(items, indent=4)


# delete item
@app.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
    token = request.args['token']
    item_id = int(id)
    if check_item(token, item_id):
        item = items_collection.find_one({'id': item_id})
        items_collection.remove(item)
        return json.dumps('Item successfully deleted'), 204
    else:
        return json.dumps('Your data do not match'), 400


def check_item(token, item_id):
    username_token_holder = collection.find_one(
        {'token': token})['username']
    username_item_holder = items_collection.find_one(
        {'id': item_id})['username']
    if username_token_holder is not None:
        return username_token_holder == username_item_holder
    else:
        return False


if __name__ == '__main__':
    app.run()

