
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
    def create_item(id, name, attr1, attr2):
        new_item = {'id' : id,
                    'name' : name,
                    'attr1' : attr1,
                    'attr2' : attr2}
        return new_item

