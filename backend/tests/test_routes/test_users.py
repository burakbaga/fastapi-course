import json 

def test_create_user(client):
    data = {"username":"testusername","email":"abc@test.com","password":"123456"}
    response = client.post("/users/",json.dumps(data))
    assert response.status_code == 200 