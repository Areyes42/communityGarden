import requests

def test_index():
    url = "http://127.0.0.1:5000/"
    response = requests.get(url)
    assert response.status_code == 200
    print("Index test passed")
    
def test_login():
    url = "http://127.0.0.1:5000/login"
    payload = {"username": "testuser", "password": "testpass"}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    try:
        response_data = response.json()
        print("Login response:", response_data)
        assert response.status_code == 200, "Login failed, status code was not 200"
        return response_data['access_token']  # Assuming JWT is returned under 'access_token' key
    except ValueError:
        print("Login response isn't JSON or JSON Decode Error")
        return None

def test_grow(access_token):
    url = "http://127.0.0.1:5000/grow"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'  # Authorization header with the JWT
    }
    response = requests.post(url, headers=headers)  # Assuming GET for this example
    try:
        response_data = response.json()
        print("User-specific action response:", response_data)
        assert response.status_code == 200, "Failed to perform user-specific action, status code was not 200"
    except ValueError:
        print("User-specific action response isn't JSON or JSON Decode Error")
 
def test_swap(access_token):
    url = "http://127.0.0.1:5000/swap"
    payload = {"task_id" : "1"}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'  # Authorization header with the JWT
    }
    response = requests.post(url, json=payload, headers=headers)  # Assuming GET for this example
    try:
        response_data = response.json()
        print("User-specific action response:", response_data)
        assert response.status_code == 200, "Failed to perform user-specific action, status code was not 200"
    except ValueError:
        print("User-specific action response isn't JSON or JSON Decode Error")
    
def test_register():
    url = "http://127.0.0.1:5000/register"
    payload = {"username": "testuser", "password": "testpass"}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    
    print(response)
    # print("Status Code:", response.status_code)
    try:
        response_data = response.json()
        print("Response Body:", response_data)
        assert response.status_code == 200, "Status code was not 200"
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        print("Response isn't JSON or JSON Decode Error")
    




if __name__ == "__main__":
    # test_index()
    # test_register()
    access_token = test_login()
    if access_token:
        test_grow(access_token)
        test_swap(access_token)