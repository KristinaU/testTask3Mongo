
# Model for User and its methods
from pymongo import collection

import app


# Model for User and its methods
class User():
    def create_user(username, password):
        new_user = {'username' : username,
                    'password' : password,
                    'token' : None,
                    'token_exp' : None}
        return new_user


# Model for Item and its methods
class Item():
    def create_item(id, username, attr1, attr2, attr3):
        new_item = {'id': id,
                    'username': username,
                    'attr1': attr1,
                    'attr2': attr2,
                    'attr3': attr3
                    }
        return new_item

