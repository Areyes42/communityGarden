from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import hashlib
import datetime
from flask_jwt_extended import create_access_token
from dtype.user import User
from flask import Flask, request, jsonify

uri = "mongodb+srv://delsterone:jVYEYXmkXofN1jH8@cluster0.xf2gegz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1')) # this is what we will use to reference the database client

db = client['community_garden']  # Database name
users = db['users']  # Collection name


def hash_password(password):
        # Return the SHA-256 hash of the password
        sha_signature = hashlib.sha256(password.encode()).hexdigest()
        return sha_signature     
    
def authenticate(username, password):

    user = users.find_one({"username": username})
    if user and user['password'] == hash_password(password):
        # Generate a JWT token
        access_token = create_access_token(identity=username)
        print("successfully authenticated!")
        return jsonify(access_token=access_token)
    else:
        print("failure to authenticate!")
        
        return jsonify({"msg": "Bad username or password"}), 401

def identity(payload):
    username = payload['username']
    return users.find_one({"username": username})

def register_user(username : str, password : str):
    if users.find_one({"username": username}) is not None:
        print("Cound not add user! Already exists")
        return
    password = hash_password(password)
    to_add = convert_user_to_document()
    users.insert_one(to_add)
    
        
def convert_user_to_document(user: User):
        doc = {"username" : f"{user.username}",
                "password": f"{user.password}", 
                "plantid": f"{user.plant_id}",
                "task_ids" : ["","","","",""]}
        return doc
        
        
class MyUser:
    def __init__(self):
        
        print("initializing user")
        username = input("Enter test username to create\n")
        password = input("Enter test password to create\n")
        password = hash_password(password)
        self.username = username
        self.password = password

    
        
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
    test_user = User("delster1", "password")
    print(authenticate("delster1", "password"))
    
main()

    
    