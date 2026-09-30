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

def import_books(books):
    print("[ * ] Importing books...")
    r = requests.post(f"{api_url}/books/import", headers=user_data["auth_header"],
            json={"books": books})
    print(r.text)
    print()

def get_books():
    print("[ * ] Getting books...")
    r = requests.get(f"{api_url}/books", headers=user_data["auth_header"])
    print(r.text)
    print()

check_api_status()
signin("Katie", "generationalgifts2019")
get_books()

book_imports = [
    {
        "title":"The Justice League",
        "author":"William Goldman",
        "year":1965,
        "pages":189
    },
    {
        "title":"The Justice League",
        "author":"William Goldman",
        "year":1975,
        "pages":189
    },
    {
        "title":"The Justice League",
        "author":"William Goldman",
        "year":1920,
        "pages":189
    }
]
#import_books(book_imports)

# Testing failed imports roll back operation:
book_imports += [
    {
        "dummy book": "dummy test",
        "dummy 1234": "something"
    },
    {
        "title": "test 21345",
        "author": "",
        "year": 1920,
        "pages": 29
    }
]
import_books(book_imports)
get_books()
signout()
