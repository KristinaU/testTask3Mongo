from pymongo import MongoClient

# pprint library is used to make the output look more pretty
from pprint import pprint


# connect to MongoDB
from app import mydb

client = MongoClient('mongodb://127.0.0.1:27017/mydb')

db=client.admin
# Issue the serverStatus command and print the results
serverStatusResult=db.command("serverStatus")
pprint(serverStatusResult)