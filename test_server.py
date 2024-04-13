import requests

def test_index():
    url = "http://localhost:5000/"
    response = requests.get(url)
    assert response.status_code == 200
    print("Index test passed")


def test_register():
    url = "http://localhost:5000/register"
    payload = {"username": "testuser", "password": "testpass"}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    
    print("Status Code:", response.status_code)
    print("Response Body:", response.json())  # Make sure your endpoint sends back JSON responses


    assert response.status_code == 200, "Status code was not 200"
    assert 'Successfully added user!' in response.json()['msg'], "User was not added successfully"
    print("Registration test passed")



if __name__ == "__main__":
    test_index()
    test_register()
