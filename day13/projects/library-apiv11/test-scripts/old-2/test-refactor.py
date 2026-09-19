import requests

api_url = "http://127.0.0.1:8000/api/v10"

user_data = {
        "username": None,
        "logged_in": False,
        "access_token": None,
        "auth_header": None
}

def new_auth_header(token):
    user_data["auth_header"] = {
        "Authorization": f"Bearer {token}"
    }
    return user_data["auth_header"]

def check_api_status():
    print("[ * ] Checking API status...")
    r = requests.get(api_url)
    print(r.text)
    print()

def signin(user_details):
    print(f"[ * ] Signing into user {user_details['username']}...")
    r = requests.post(f"{api_url}/signin", data=user_details)
    print(r.text)
    print()
    if r.status_code == 200:
        response = r.json()
        user_data["username"] = user_details["username"]
        user_data["access_token"] = response["access_token"]
        user_data["logged_in"] = True
        new_auth_header(response["access_token"])

def signup(user_detail):
    print(f"[ * ] Signing up at as user {user_detail['username']}...")
    r = requests.post(f"{api_url}/signup", json=user_detail)
    print(r.text)
    print()

def signout():
    if user_data["logged_in"]:
        print(f"[ * ] Signing out of user {user_data['username']}...")
        user_data["username"] = None
        user_data["logged_in"] = False
        user_data["access_token"] = None
        user_data["auth_header"] = None
        return
    print("[ * ] Not signed in...")

signin({"username": "Katie", "password": "generationalgifts"})
signin({"username": "Katie", "password": "generationalgifts2019"})
user_details = {
    "username": "User 101",
    "fullname": "New User",
    "password": "test1234",
    "password_confirmation": "test1234"
}
signup(user_details)
