from flask import Flask, request, redirect, url_for, render_template
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, set_access_cookies, unset_access_cookies
from database import authenticate, register_user, update_plant, swap_user_task, set_new_user_tasks, get_user_plant, get_user_tasks, get_all_user_plants
from flask import jsonify
from plantgen import generate_garden, grow_plant
from datetime import timedelta

# from database import authenticate

app = Flask(__name__)
jwt = JWTManager(app)
app.config['SECRET_KEY'] = "asdkjfhaskjdfhasiudfhasiudfuinyvulih324"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1) 
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'

@app.route('/<path:filename>')
def send_file(filename):
    return app.send_static_file(filename)

@app.route('/gardenplant/<username>', methods=["GET"])
def user_gardenplant(username):
    plant = get_user_plant(username)
    print("PLANT: ", plant)
    return jsonify({"message": "Retrieved Plant", "username": username, "plant": plant })

@app.route('/garden/<username>', methods=["GET"])
def user_garden(username):
    return render_template('usergarden.html', username=username)
# should be the plant homepage
@app.route('/')
@jwt_required()
def index():
    current_user = get_jwt_identity()
    tasks = get_user_tasks(current_user)
    return render_template('index.html', username=current_user, tasks=tasks)

# @app.before_request
# def log_request_info():
#     app.logger.debug('Headers: %s', request.headers)
#     app.logger.debug('Cookies: %s', request.cookies)
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
            response = jsonify({'login': True, 'msg': 'Login successful'})
            # Set the JWT in an HTTPOnly cookie securely
            set_access_cookies(response, access_token)
            return response
        else:
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
        return app.send_static_file("login/login.html")

# shows the garden of other users!
@app.route('/garden')
def garden():
    return render_template('garden.html')

@app.route('/get_garden', methods=['GET'])
def get_garden():
    usernames, plants = get_all_user_plants()
    print("USERNAMES: ",usernames)
    print("PLANTS: ", plants)
    return jsonify({"usernames": usernames, "plants": plants})

@app.route('/add', methods=['GET','POST'])
@jwt_required()
def set_tasks():
    current_user = get_jwt_identity()
    set_user_tasks(current_user)
    return app.send_static_file('index.html')
    
@app.route('/tasks', methods=["GET", 'POST'])
@jwt_required()
def tasks_site():
    if request.method == "GET":
        current_user = get_jwt_identity()
        current_tasks = get_user_tasks(current_user)
        print("TASKS: ", current_tasks)
        return render_template("tasks_site.html", tasks=current_tasks, current_user = current_user)
@app.route('/logout', methods=['GET'])
def logout():
    response = jsonify({'logout': True, 'msg': 'Logout successful'})
    unset_access_cookies(response)
    return response

# Swap task endpoint for user to change a task from their personal checklist
# @app.route('/swap', methods=['POST'])
# @jwt_required()
# def swap():
#     print("Headers:", request.headers)
#     print("Cookies:", request.cookies)
#     current_user = get_jwt_identity()
#     print("TO SWAP: ")
    
#     to_swap = request.json.get("task_id")
#     swap_user_task(current_user, to_swap)
#     return app.send_static_file('index.html')

# Grow user's plant
@app.route('/grow/<username>', methods=['POST'])
def grow(username):
    current_plant = get_user_plant(username)
    new_plant = grow_plant(current_plant, 1)
    update_plant(username, new_plant)
    return app.send_static_file('index.html')

@app.route('/swap/<username>/', methods=['POST'])
def swap(username):
    data = request.get_json()
    task_id = data["task_id"]
    task_id = task_id.strip()
    print("TASK ID:", task_id)
    response, code =  swap_user_task(username, task_id)
    return response


@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return app.send_static_file('404/404.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

