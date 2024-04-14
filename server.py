from flask import Flask, request, url_for
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from database import authenticate, register_user, update_plant, swap_user_task, set_new_user_tasks, get_user_plant, get_user_tasks
from flask import jsonify
from plantgen import generate_garden
# from database import authenticate

app = Flask(__name__)
jwt = JWTManager(app)
app.config['SECRET_KEY'] = "asdkjfhaskjdfhasiudfhasiudfuinyvulih324"

@app.route('/<path:filename>')
def send_file(filename):
    return app.send_static_file(filename)

@app.route('/garden/<username>', methods=["GET"])
def user_garden(username):
    plant = get_user_plant(username)
    if len(plant) > 1: # error when length of plant greater than 1
        return plant
    return jsonify({"message": "Retrieved Plant", "username": username, "plant": plant })
# should be the plant homepage
@app.route('/')
@jwt_required()
def index():
    print("INDEX")
    current_user = get_jwt_identity()
    plant = get_user_plant(current_user)
    tasks = get_user_tasks(current_user)
    # return index.html from static folder
    return render_template('index.html', plant=plant, tasks=tasks)

# get the templates from mongodb and display them
@app.route('/templates')
def templates():
    return app.send_static_file('templates.html')

# login page
# create_access_token() function is used to actually generate the JWT, this function is in database
@app.route("/login", methods=['GET',"POST"])
def login():
    if request.method == "GET":
        return app.send_static_file("login/login.html")
    elif request.method == "POST":
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        access_token, status_code = authenticate(username, password)
        if status_code == 200:
            # Redirect to the home page
            return redirect(url_for('index'))
        else:
            return response, status_code

    return app.send_static_file('login/login.html')

# registers a user into the db
@app.route('/register', methods=['GET',"POST"])
def register():
    if request.method == "POST":
        print("REGISTER called")
        data = request.get_json()
        username = data['username']
        password = data['password']
        register_user(username, password)
        set_new_user_tasks(username)
        return jsonify({"message": "User registered", "username": username})

# shows the garden of other users!
@app.route('/garden')
def garden():
    return app.send_static_file('garden/garden.html')

@app.route('/get_garden', methods=['GET'])
def get_garden():
    return ','.join(generate_garden(6, 4))

@app.route('/add', methods=['POST'])
@jwt_required()
def set_tasks():
    current_user = get_jwt_identity()
    set_user_tasks(current_user)
    return app.send_static_file('index.html')
    
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

