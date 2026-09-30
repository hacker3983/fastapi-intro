import requests

api_url = "http://localhost:8000/api/v12"
user_data = {
        "username": None,
        "access_token": None,
        "auth_header": None, 
        "logged_in": False
}

def check_api_status():
    print("[ * ] Checking API status...")
    r = requests.get("http://localhost:8000")
    print(r.text)
    print()

def new_auth_header(token):
    user_data["access_token"] = token
    user_data["auth_header"] = {
        "Authorization": f"Bearer {token}"
    }
    return user_data["auth_header"]

def signup(user_detail):
    print(f"[ * ] Signing up as user {user_detail['username']}...")
    r = requests.post(f"{api_url}/signup", json=user_detail)
    print(r.text)
    print()


def signin(username, password):
    print(f"[ * ] Signing into user account {username}...")
    r = requests.post(f"{api_url}/signin", data={"username": username, "password": password})
    print(r.text)
    print()
    response = r.json()
    if r.status_code == 200:
        user_data["username"] = username
        new_auth_header(response["access_token"])
        user_data["logged_in"] = True

def signout():
    if user_data["logged_in"]:
        print(f"[ * ] Signing out of user account {user_data['username']}...")
        user_data["logged_in"] = False
        user_data["auth_header"] = None
        user_data["access_token"] = None
        return
    print("[ * ] Not signed in...")

def get_books():
    print("[ * ] Getting books...")
    r = requests.get(f"{api_url}/books", headers=user_data["auth_header"])
    print(r.text)
    print()

def get_book_by_id(book_id):
    print("[ * ] Getting books...")
    r = requests.get(f"{api_url}/books/{book_id}", headers=user_data["auth_header"])
    print(r.text)
    print()

def get_user(user_id):
    print(f"[ * ] Getting user by id {user_id}...")
    r = requests.get(f"{api_url}/users/{user_id}", headers=user_data["auth_header"])
    print(r.text)
    print()

user_details = {
    "username": "Anonymous",
    "fullname": "Anonymous User",
    "password": "test1234",
    "password_confirmation": "test1234"
}
signup(user_details)

user_details["username"] = "Newuser1981"
signup(user_details)
password = user_details["password"]
user_details["password"] = password[:4]
signup(user_details)

signin("Newuser1981", "test1234")
signin("Newuser1981", "test123")
signin("0000", "test1234")

original_token = user_data["access_token"]

new_auth_header("dumbshit 21")
get_books()

new_auth_header("")
get_books()

new_auth_header(original_token)
get_user(1)

signin("Katie", "generationalgifts2019")
get_user(1)

signin("John", "test1234")
get_user(3)

signin("Newuser1981", "test1234")
get_book_by_id(71)
