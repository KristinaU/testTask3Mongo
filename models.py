
# Model for User and its methods
from pymongo import collection

import app


class User():
    def create_user(username, password):
        new_user = {'username' : username,
                    'password' : password,
                    'token' : None,
                    'token_exp' : None}
        return new_user


    def set_token(self, token, token_exp):
        self.set({'token' : token})
        self.set({'token_exp': token_exp})
        return self


# Model for Item and its methods
class Item():
    def create_item(id, name, attr1):
        return True, 200