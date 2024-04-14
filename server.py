from flask import Flask, request, redirect, url_for, render_template
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, set_access_cookies
from database import authenticate, register_user, update_plant, swap_user_task, set_new_user_tasks, get_user_plant, get_user_tasks, get_all_usernames
from flask import jsonify
from plantgen import generate_garden
# from database import authenticate

app = Flask(__name__)
jwt = JWTManager(app)
app.config['SECRET_KEY'] = "asdkjfhaskjdfhasiudfhasiudfuinyvulih324"
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
@app.route('/<path:filename>')
def send_file(filename):
    return app.send_static_file(filename)

@app.route('/garden/<username>', methods=["GET"])
def user_garden(username):
    plant = get_user_plant(username)
    print("PLANT: ", plant)
    if len(plant) > 1: 
        return plant
    return jsonify({"message": "Retrieved Plant", "username": username, "plant": plant })
# should be the plant homepage
@app.route('/')
@jwt_required()
def index():
    current_user = get_jwt_identity()
    plant = get_user_plant(current_user)
    tasks = get_user_tasks(current_user)
    return render_template('index.html', username=current_user, plant=plant, tasks=tasks)

@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Cookies: %s', request.cookies)
# get the templates from mongodb and display them
@app.route('/templates')
def templates():
    return app.send_static_file('templates.html')

# login page
# create_access_token() function is used to actually generate the JWT, this function is in database
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return app.send_static_file("login/login.html")
    elif request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        response, status_code = authenticate(username, password)

        if status_code == 200:
            # Extract the token from the JSON response
            access_token = response.get_json()['access_token']
            print("Access Token:", access_token)
            response = jsonify({'login': True, 'msg': 'Login successful'})
            set_access_cookies(response, access_token)  # Set the JWT in an HTTPOnly cookie
            # Redirect to index with token as URL parameter (not recommended, shown for completion)
            return redirect(url_for('index'))
        else:
            # Return the error response if authentication fails
            return response, status_code

# registers a user into the db
@app.route('/register', methods=['GET',"POST"])
def register():
    if request.method == "GET":
        return app.send_static_file("register/register.html")
    if request.method == "POST":
        print("REGISTER called")
        data = request.get_json()
        username = data['username']
        password = data['password']
        register_user(username, password)
        set_new_user_tasks(username)
        return redirect(url_for('index'))

from database import users
# shows the garden of other users!
@app.route('/garden')
def garden():
    usernames = get_all_usernames()
    print("USERNAMES: ",usernames)
    return render_template('garden.html', users=usernames)

@app.route('/get_garden', methods=['GET'])
def get_garden():
    return ','.join(generate_garden(8, 2))

@app.route('/add', methods=['GET','POST'])
@jwt_required()
def set_tasks():
    current_user = get_jwt_identity()
    set_user_tasks(current_user)
    return app.send_static_file('index.html')
    
@app.route('/tasks', methods=["GET", 'POST'])
@jwt_required
def render_tasks():
    current_user = get_jwt_identity()
    current_tasks = get_user_tasks(current_user)
    print(current_tasks)
    
    return render_template("tasks.html", tasks=current_tasks)
@app.route('/logout', methods=['GET'])
def logout():
    response = jsonify({'logout': True, 'msg': 'Logout successful'})
    unset_jwt_cookies(response)
    return response
# Swap task endpoint for user to change a task from their personal checklist
@app.route('/swap', methods=['POST'])
@jwt_required()
def swap_task():
    to_swap = request.json.get("task_id")
    current_user = get_jwt_identity()
    swap_user_task(current_user, to_swap)
    return app.send_static_file('index.html')

# Grow user's plant
@app.route('/grow', methods=['POST'])
@jwt_required()
def grow():
    current_user = get_jwt_identity()
    update_plant(current_user, "test")
    return app.send_static_file('index.html')

# Add water to user's plant
@app.route('/water', methods=['POST'])
@jwt_required()
def water():
    update_plant(current_user, "test")
    return app.send_static_file('index.html')

# Add sunlight to user's plant
@app.route('/sunlight', methods=['POST'])
@jwt_required()
def sunlight():
    update_plant(current_user, "test")
    return app.send_static_file('index.html')



@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return app.send_static_file('404/404.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

