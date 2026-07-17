import requests

api_url = "http://127.0.0.1:8000"
token_cache = {}
user_data = {
        "username": None,
        "access_token": None,
        "logged_in": False,
        "auth_header": None
}

def new_auth_header(access_token):
    global user_data
    user_data["auth_header"] = {"Authorization": f"Bearer {access_token}"}
    return user_data["auth_header"]

def get_user_by_token(access_token):
    usernames = list(token_cache)
    access_tokens = list(token_cache.values())
    username_index = access_tokens.index(access_token)
    username = usernames[username_index]
    return username

def check_api_stats():
    print("[ * ] Checking API Status...")
    r = requests.get(f"{api_url}")
    print(r.text)
    print()

def signup(user_details):
    print(f"[ * ] Creating user account {user_details['username']}...")
    r = requests.post(f"{api_url}/signup",
            json=user_details
    )
    print(r.text)
    print()

def create_accounts(users_list):
    for user_details in users_list:
        signup(user_details)

def login(username, password):
    print(f"[ * ] Logging into user account {username}...")
    r = requests.post(f"{api_url}/token", data={"username": username, "password": password})
    print(r.text)
    print()
    response = r.json()
    if r.status_code == 200:
        token_cache.update({username: response["access_token"]})
        user_data["username"] = username
        user_data["access_token"] = response["access_token"]
        new_auth_header(response["access_token"])
        user_data["logged_in"] = True
        return response
    return None

def retrieve_details():
    print(f"[ * ] Retrieving details for user {user_data['username']}...")
    r = requests.get(f"{api_url}/details", headers=user_data['auth_header'])
    print(r.text)
    print()

def update_details(user_details):
    print(f"[ * ] Updating details for user {user_data['username']}...")
    r = requests.put(f"{api_url}/update", headers=user_data['auth_header'], json=user_details)
    response = r.json()
    new_username = user_details.get("username")
    if new_username and r.status_code == 200:
        old_username = user_data['username']
        user_data['username'] = new_username
        token_cache[new_username] = token_cache.pop(old_username)
        print("Updated username...")
    print(r.text)
    print()

def delete_user_account():
    print(f"[ * ] Deleting user account for user {user_data['username']}")
    r = requests.delete(f"{api_url}/delete", headers=user_data['auth_header'])
    print(r.text)
    print()

def logout():
    print(f"[ * ] Logging out of user {user_data['username']}...")
    user_data['access_token'] = None
    user_data['auth_header'] = None
    user_data['logged_in'] = False
    print()

users_list = [
    {
        "username": "Alex",
        "password": "Secret1234",
        "password_confirmation": "Secret1234",
        "age": 10,
        "occupation": "Student",
        "birth_year": 2016,
        "birth_month": 10,
        "birth_day": 8
    },
    {
        "username": "Katie",
        "password": "Superfast1981",
        "password_confirmation": "Superfast1981",
        "age": 10,
        "occupation": "Student",
        "birth_year": 2016,
        "birth_month": 10,
        "birth_day": 10
    },
    {
        "username": "Dujohn",
        "password": "SuperSecret2015",
        "password_confirmation": "SuperSecret2015",
        "age": 18,
        "occupation": "Software Engineer (Backend Developer)",
        "birth_year": 2007,
        "birth_month": 10,
        "birth_day": 8
    },
    {
        "username": "Debra",
        "password": "SecretLover27",
        "password_confirmation": "SecretLover27",
        "age": 18,
        "occupation": "It Support Specialist",
        "birth_year": 2007,
        "birth_month": 10,
        "birth_day": 22
    }
]

check_api_stats()
create_accounts(users_list)
login("Alex", "Secret1234")
retrieve_details()
update_details({"username": "Katie"})
update_details({"username": "Max", "password": "somethingelse"})
modified_details = {
    "username": "Max",
    "occupation": "Doctor",
    "age": 22,
    "birth_year": 2004,
    "birth_month": 12,
    "birth_day": 15
}
update_details(modified_details)
login("Max", "somethingelse")
update_details(modified_details)
modified_details.pop("username")
update_details(modified_details)
retrieve_details()
delete_user_account()

login("Max", "somethingelse")
login("Katie", "Superfast1981")
retrieve_details()
update_details({})
delete_user_account()

login("Debra", "SecretLover27")
update_details({})
retrieve_details()

login("Dujohn", "SuperSecret2015")
update_details({})
retrieve_details()

user_copy = users_list[0].copy()
user_copy["password_confirmation"] += "a" * 3
signup(user_copy)

signup(users_list[3])
login("Alex", "test1234")

retrieve_details()
logout()

retrieve_details()
