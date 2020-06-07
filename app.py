from flask import Flask, request
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)


@app.route('/')
def index():
    return 'Index Page'


@app.route('/hello')
def hello_world():
    return 'Hello World!'


# registration
@app.route('/registration', methods=['POST'])
def registration():
    if create_user(request.form['username'], request.form['password']):
        return 'yeah haaahhh', 200

    else:
        return 'Ohh nooo', 400


def create_user(username, password):
#    new_user = {'username': username, 'password': password, 'token' : 1223}
    return True

if __name__ == '__main__':
    app.run()
