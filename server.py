from flask import Flask, render_template

app = Flask(__name__)

@app.route('/<path:filename>')
def send_file(filename):
    return app.send_static_file(filename)

# Define the root endpoint
@app.route('/')
def index():
    # return index.html from static folder
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

