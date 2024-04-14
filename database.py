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
tasks = db['tasks']

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
        return jsonify(access_token=access_token), 200
    else:
        print("failure to authenticate!")
        
        return jsonify({"msg": "Bad username or password"}), 401

def register_user(username: str, password: str):
    print(f"GOT USER! {username}, {password}")
    if users.find_one({"username": username}) is not None:
        return jsonify({"msg": "Couldn't add user! Already exists"}), 401
    hashed_password = hash_password(password)
    to_add = convert_user_to_document(username, hashed_password)
    users.insert_one(to_add)
    return jsonify({"msg": "Successfully added user!"}), 200
    
def update_plant(username : str, plant_id : str):
    if users.find_one({"username": username}) is None:
        return jsonify({"msg": "Couldn't edit user! User doesn't exist!"}), 401
    users.update_one(
        {"username": username},  # Query document to find the user
        {"$set": {"plant_id": plant_id}}  # Update operation
    )

    return jsonify({"msg": "Successfully updated plant id!"}), 200
def get_random_task():
    pipeline = [
        {"$sample": {"size": 1}}  # Randomly select 1 document
    ]
    result = list(tasks.aggregate(pipeline))
    if result:
        return result[0]  # Return the document
    else:
        return None  # No document found
def swap_task(username:str, task_id: str):
    new_task = get_random_task()
    if users.find_one({"task_id" : task_id}) is None:
        return jsonify({"msg": "Couldn't edit task, doesn't exist!"})
    users.update_one(
        {"username": username},
        {"$set": {task_id : new_task}}
    )
def convert_user_to_document(username, password):
        doc = {"username" : f"{username}",
                "password": f"{password}", 
                "plant_id": "",
                "task_ids" : ["","","","",""]}
        return doc
        
        
def main():

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    test_user = User("delster1", "password")
    print(authenticate("delster1", "password"))
    
# main()

    
    