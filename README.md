# testTask3Mongo
Another try to create an API for OW, now with MongoDB

Python 3.6.10

Flask 1.1.2

db: MongoDB

Queries and responces format: JSON

<h3>Models:</h3>

User: {
<br>username     // identification field, uniqueness checked on registration step
       <br>
       password  // stored plain
       <br>
       token     // authentification token
       <br>
       token_exp // time when a token is expired, stored but currently not in use
       <br>
       }
       
Item: {
<br>
       id        // unique iterating integer number to identificate items
       <br>
       username  // foreign key to set many to one relationship with Users
       <br>
       item_name // item_name, might be not unique
       <br>
       }
       

<h3>Methods allowed:</h3>

/registration: [POST] args: [username] [password], check: if username already exists, return: "Success!"

/login: [POST] args: [username] [password], check: username and password match, return: temporary token

/items/new: [POST] args: temporary token, check: find user with this token, return: item created, item attributes

/items: [GET] args: temporary token, check: find user with this token, return: items for this user with their attributes

/items/:id [DELETE]: args: temporary token, check: if token holder is actually item holder, return: Message 'Deleted'

<h3>Testing:</h3>

Unit tests provided for Models.<br>App functionality has been tested with <b>Postman</b>
