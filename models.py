
# Model for User and its methods
from pymongo import collection

import app


# Model for User
# primary key : 'username' which is checked
# for uniqueness at registration stage
class User():
    def create_user(username, password):
        new_user = {'username' : username,
                    'password' : password,
                    'token' : None,
                    'token_exp' : None}
        return new_user


# Model for Item
# primary key: 'id' which is int and unique
# foreign key: 'username'
class Item():
    def create_item(id, username, item_name):
        new_item = {'id': id,
                    'username': username,
                    'item_name': item_name,
                    }
        return new_item

