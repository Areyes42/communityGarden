from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import hashlib
import datetime
from flask_jwt_extended import create_access_token
from dtype.user import User
from flask import Flask, request, jsonify
from plantgen import generate_garden


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
def get_all_user_plants():
    usernames = []
    plants = []
    # Fetch all users' documents
    all_users = users.find()  # This returns a cursor to iterate over all documents

    for user in all_users:
        username = user.get('username')
        plant = user.get('plant_id')
        usernames.append(username)
        plants.append(plant)

    return usernames, plants
def register_user(username: str, password: str):
    print(f"GOT USER! {username}, {password}")
    if users.find_one({"username": username}) is not None:
        return jsonify({"msg": "Couldn't add user! Already exists"}), 401
    plant = generate_garden(1,1)[0]
    hashed_password = hash_password(password)
    to_add = convert_user_to_document(username, hashed_password, plant)
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
    
def get_user_plant(username: str):
    # Query the database for the user by username
    user_document = users.find_one({"username": username})

    # If the user is found, retrieve their plant data
    if user_document:
        plant_data = user_document.get('plant_data')
        print(plant_data)
        return plant_data
    else:
        # No user was found with this username
        return jsonify({"msg": "User not found."}), 404
 
def get_user_tasks(username: str):
    user_document = users.find_one({"username": username})
    
    if user_document:
        tasks = user_document.get('tasks')   
        return tasks
    else:
        return jsonify({"msg": "User not found."}), 404
        
def set_new_user_tasks(username: str):
    user_document = users.find_one({"username": username})
    if user_document:
        new_tasks = []
        for i in range(5):
            task = get_random_task()
            if task is not None:
                new_tasks.append(task)
        users.update_one(
            {"username": username},  # Match the user by username
            {"$set": {"tasks": new_tasks}}  # Set the new tasks
        )
        return jsonify({"msg": "Updated user tasks!"}), 200
    return jsonify({"msg": "User not found."}), 404
    
        
def swap_user_task(username: str, task_id : str):
    print("swapping user task")
    user = users.find_one({"username": username}, {"tasks": 1})
    if user is None:
        return jsonify({"msg": "User not found!"}), 404
    print(task_id)
    # Get the user's current tasks
    current_tasks = user.get('tasks', [])
    # Check if the task_id to be replaced exists in the user's tasks
    task_ids = [str(task.get('task_id')) for task in current_tasks]  # Convert ObjectIds to strings if necessary
    
    
    # Get a new random task
    new_task = get_random_task()
    # If the task_id does not need to be preserved, you can omit this step.
    # Otherwise, make sure to set the correct 'task_id' field in the new task
    new_task['task_id'] = task_id
    
    # Swap out the old task for the new one
    new_tasks = []
    for task in current_tasks:
        if task_id in str(task):
            print("FOUND TASK TO EDIT")
            new_tasks.append(new_task)
        else:
            new_tasks.append(task)
    # Update the user's tasks in the database
    print(new_tasks)
    
    update_result = users.update_one(
        {"username": username},
        {"$set": {"tasks": new_tasks}}
    )
    # Check if the update was successful
    if update_result.modified_count > 0:
        return jsonify({"msg": "Task updated successfully!"}), 200
    else:
        return jsonify({"msg": "No update was made, please check the task details."}), 400
    
def convert_user_to_document(username, password, plant_id):
        doc = {"username" : f"{username}",
                "password": f"{password}", 
                "plant_id": plant_id,
                "tasks" : ["","","","",""]}
        return doc
        
        
def main():

    # Send a ping to confirm a successful connection
    get_user_plant("testuser")
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
   
        
# main()

    
    
