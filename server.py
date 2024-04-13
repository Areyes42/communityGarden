from flask import Flask
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
# from database import authenticate

app = Flask(__name__)
# JWT = JWTManager(app, authenticate)

@app.route('/<path:filename>')
def send_file(filename):
    return app.send_static_file(filename)

# should be the plant homepage
@app.route('/')
@jwt_required()
def index():
    # return index.html from static folder
    return app.send_static_file('index.html')

# get the templates from mongodb and display them
@app.route('/templates')
def templates():
    return app.send_static_file('templates.html')

# login page
@app.route('/login')
def login():
    return app.send_static_file('login.html')

# registers a user into the db
@app.route('/register')
def register():
    return app.send_static_file('register.html')

# shows the garden of other users!
@app.route('/garden')
def garden():
    return app.send_static_file('garden.html')

# Add task endpoint for user to add task to their personal checklist
@app.route('/add', methods=['POST'])
@jwt_required()
def add_task():
    current_user = get_jwt_identity()
    return app.send_static_file('index.html')

# Delete task endpoint for user to remove task from their personal checklist
@app.route('/delete', methods=['POST'])
@jwt_required()
def delete_task():
    current_user = get_jwt_identity()
    return app.send_static_file('index.html')

# Grow user's plant
@app.route('/grow', methods=['POST'])
@jwt_required()
def grow():
    return app.send_static_file('index.html')

# Add water to user's plant
@app.route('/water', methods=['POST'])
@jwt_required()
def water():
    return app.send_static_file('index.html')

# Add sunlight to user's plant
@app.route('/sunlight', methods=['POST'])
@jwt_required()
def sunlight():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

