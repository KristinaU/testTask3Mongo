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
db.item_counter.insert({'seq': 0})
items_collection = db["items_collection"]


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
    user = models.User.create_user(
        request.form['username'],
        request.form['password']
    )
    collection.insert(user)
    #   add errors handler
    return 'User register success!', 200


# list of all users
@app.route('/users', methods=['GET'])
def users():
    result = 'So we got the users as: ' + (
        str(collection.distinct('username'))
    )
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

            {'username': request.form['username']},

            {"$set": {'token': token, 'token_exp': expiry_time}}

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


def getCount(item_counter,name):
   return item_counter.find_and_modify( update= { '$inc': {'seq': 1}},
                                        new=True ).get('seq')


# add item
@app.route('/items/new', methods=['POST'])
def add_item():
    item_holder_username = collection.find_one(
        {'token': request.form['token']})['username']
    item = models.Item.create_item(
          getCount(db.item_counter, "seq"),
          item_holder_username, request.form['attr1'],
          request.form['attr2'], request.form['attr3']
    )
    items_collection.insert(item)
    #   add errors handler
    result = str(item)
    return 'Item added! Its attributes are: ' + result, 200


# get items
@app.route('/items/', methods=['GET'])
def items():
    current_username = collection.find_one(
        {'token': request.form['token']})['username']
    items = list(items_collection.find({'username': current_username}))
    #   add error handler
    return str(items)



# delete item
#@app.route('/items/:id', methods=['DELETE'])
#def delete_item():

#    print (request.form['token'], request.form['id'])
#    token = request.form['token']
#    item_id = request.form['id']
#    if check_item(token, item_id):
#        item = items_collection.find_one({'id': item_id})
#        items_collection.remove(item)
#        return 'Item successfully deleted', 200
#    else:
#        return 'Your data do not match', 400


#def check_item(token, item_id):
#    user_token_holder = items_collection.find_one({'token': token})
#    user_item_holder = items_collection.find_one({'id': item_id})

#    print (str(user_token_holder))
#    print(str(user_item_holder))

#    return user_token_holder == user_item_holder


if __name__ == '__main__':
    app.run()
