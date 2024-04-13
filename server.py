from flask import Flask

app = Flask(__name__)

@app.route('/<path:filename>')
def send_file(filename):
    return app.send_static_file(filename)

# Define the root endpoint
# should be the plant homepage
@app.route('/')
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

# get garden from db to send to garden page
@app.route('/get_garden', methods=['GET'])
def get_garden():
    return app.send_static_file('index.html')

# Add task endpoint for user to add task to their personal checklist
@app.route('/add', methods=['POST'])
def add_task():
    return app.send_static_file('index.html')

# Delete task endpoint for user to remove task from their personal checklist
@app.route('/delete', methods=['POST'])
def delete_task():
    return app.send_static_file('index.html')

# Add template to db
@app.route('/add_template', methods=['POST'])
def add_template():
    return app.send_static_file('index.html')

# Delete template from db
@app.route('/delete_template', methods=['POST'])
def delete_template():
    return app.send_static_file('index.html')

# Grow user's plant
@app.route('/grow', methods=['POST'])
def grow():
    return app.send_static_file('index.html')

# Add water to user's plant
@app.route('/water', methods=['POST'])
def water():
    return app.send_static_file('index.html')

# Add sunlight to user's plant
@app.route('/sunlight', methods=['POST'])
def sunlight():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

