from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import hashlib

from flask import Flask, request, jsonify

uri = "mongodb+srv://delsterone:jVYEYXmkXofN1jH8@cluster0.xf2gegz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1')) # this is what we will use to reference the database client

db = client['community_garden']  # Database name
users = db['users']  # Collection name
def hash_password(password):
        # Return the SHA-256 hash of the password
        sha_signature = hashlib.sha256(password.encode()).hexdigest()
        return sha_signature   
    
def login():
    username = input("Enter username")
    password = input("Enter password")
    user = users.find_one({"username": username})

    if user and user['password'] == hash_password(password):
        print("successful!")
    else:
        print("unsuccessful")
    
class User:
    def __init__(self):
        
        print("initializing user")
        username = input("Enter test username to create\n")
        password = input("Enter test password to create\n")
        password = hash_password(password)
        self.username = username
        self.password = password

    def add_user_to_database(self):
        to_add = self.write_user_to_document()
        users.insert_one(to_add)
        
    
    
    def write_user_to_document(self):
        return { "username" : f"{self.username}", "password": f"{self.password}"}
    
    def __repr__(self):
        return f"{self.username}, {self.password}"

def main():

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    # my_user = User()
    # print(my_user)
    # my_user.add_user_to_database()
    # print(users)
    login()
    users.drop()
main()

    
    