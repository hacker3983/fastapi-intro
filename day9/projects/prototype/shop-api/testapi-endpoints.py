import requests

token_cache = {}
user_data = {
    "username": None,
    "logged_in": False,
    "auth_header": None
}

api_url = "http://localhost:8000"

def new_auth_header(access_token):
    global user_data
    user_data["auth_header"] = {"Authorization": f"Bearer {access_token}"}
    return user_data["auth_header"]

def check_api_stats():
    print("[ * ] CHecking api status...")
    r = requests.get(f"{api_url}")
    print(r.text)
    print()

def signup(user_details):
    print(f"[ * ] Creating user account {user_details['username']}...")
    r = requests.post(f"{api_url}/signup", json=user_details)
    print(r.text)
    print()

def create_accounts(users_list):
    for user_details in users_list:
        user_details["password_confirmation"] = user_details["password"]
        signup(user_details)

def signin(user_details):
    print(f"[ * ] Signing into user {user_details['username']}...")
    r = requests.post(f"{api_url}/signin", data=user_details)
    print(r.text)
    print()
    response = None
    if r.status_code == 200:
        response = r.json()
        user_data["username"] = user_details["username"]
        user_data["access_token"] = response["access_token"]
        new_auth_header(response["access_token"])
        user_data["logged_in"] = True
    return response

def logout():
    if user_data['logged_in']:
        print(f"[ * ] Logging out of user {user_data['username']}...")
        user_data['username'] = None
        user_data['access_token'] = None
        user_data['auth_header'] = None
        user_data['logged_in'] = False
        return
    print("[ * ] Not logged in...")

def create_product(product_details):
    print(f"[ * ] Creating product {product_details['name']} for user {user_data['username']}...")
    r = requests.post(f"{api_url}/products", json=product_details, headers=user_data['auth_header'])
    print(r.text)
    print()

def create_products(users_list, products_list):
    for i, user in enumerate(users_list):
        username = user['username']
        password = user['password']
        print(f"[ * ] Signing into user {username} to create products...")
        signin({"username": username, "password": password})
        products = products_list[username]
        for product in products:
            create_product(product)

def get_products():
    print(f"[ * ] Getting products...")
    r = requests.get(f"{api_url}/products", headers=user_data['auth_header'])
    print(r.text)
    print()

def get_product(product_id):
    print(f"[ * ] Getting product by id {product_id}...")
    r = requests.get(f"{api_url}/products/{product_id}", headers=user_data['auth_header'])
    print(r.text)
    print()

def update_product(product_id, product_details):
    print(f"[ * ] Updating product by id {product_id}...")
    name = product_details.get("name")
    if name:
        print(f"Updating with name {name}")

    description = product_details.get("description")
    if description:
        print(f"Updating with description:")
        print(description)

    value = product_details.get("value")
    if value:
        print("Updating with value:", value)
    r = requests.put(f"{api_url}/products/{product_id}", json=product_details,
            headers=user_data['auth_header'])
    print(r.text)
    print()

def delete_product(product_id):
    print(f"[ * ] Deleting product by id {product_id}...")
    r = requests.delete(f"{api_url}/products/{product_id}",
            headers=user_data['auth_header'])
    print(r.text)
    print()

def get_product_count():
    print(f"[ * ] Getting product count for user {user_data['username']}")
    r = requests.get(f"{api_url}/count", headers=user_data['auth_header'])
    print(r.text)
    print()

users_list = [
    {
        "username": "John",
        "full_name": "John Doe",
        "password": "test1234"
    },
    {
        "username": "Katie",
        "full_name": "Katie Williams",
        "password": "generationalgifts2019"
    },
    {
        "username": "Max",
        "full_name": "Max Carter",
        "password": "petroleumjelly1981"
    },
    {
        "username": "Alex",
        "full_name": "Alex Doe",
        "password": "alexis1934"
    }
]
products_list = {
    "John": [
        {
            "name": "Bread",
            "description": "Just some bread bro!",
            "value": 560
        },
        {
            "name": "Cheese",
            "description": "Just some cheese!",
            "value": 120
        },
        {
            "name": "Bulla",
            "description": "Just some bulla bro!",
            "value": 50
        },
        {
            "name": "Flour",
            "description": "Just some flour bro!",
            "value": 70
        }
    ],
    "Katie": [
        {
            "name": "Apple",
            "description": "A fruit that grows on trees and contains seed!",
            "value": 100
        },
        {
            "name": "Banana",
            "description": "A tuber fruit that grows on a tree!",
            "value": 50
        },
        {
            "name": "Cherry",
            "description": "A small fruit that grows on trees",
            "value": 30
        },
        {
            "name": "PineApple",
            "description": "A fruit that is normally yellow and grows underneath the earth!",
            "value": 200
        }
    ],
    "Max": [
        {
            "name": "Cup Cakes",
            "description": "Some small cakes that normally come in a small packet!",
            "value": 50
        },
        {
            "name": "Wine Cakes",
            "description": "A made up of wine!",
            "value": 150
        },
        {
            "name": "Banana Bread",
            "description": "A cake made up of banana!",
            "value": 120
        },
        {
            "name": "Black Forest",
            "description": "A cake made up of chocolate, alcohol and cherries on top!",
            "value": 1500
        }
    ],
    "Alex": [
        {
            "name": "Guava Juice",
            "description": "A juice made up of guava fruit!",
            "value": 300
        },
        {
            "name": "June Plum Juice",
            "description": "A juice made up of june plums!",
            "value": 200
        },
        {
            "name": "Pineapple Juice",
            "description": "A juice made from pineapple!",
            "value": 500
        },
        {
            "name": "Cherry Juice",
            "description": "A juice made up of Cherry!",
            "value": 150
        }
    ]
}
create_accounts(users_list)
create_products(users_list, products_list)
signin({"username": "John", "password": "test1234"})
signin({"username": "John", "password": "wrongpassword"})
signin({"username": "Alex", "password": "invaliduser1234"})
user_data['auth_header']["Authorization"] = "Bearer somethingsomething"
get_products()
signin({"username": "John", "password": "test1234"})
get_products()
get_product(1)
get_product(0)
get_product(2)
update_product(5, {"name": "nothing"})
update_product(1, {"name": "Cheese", "description": "A product made of flour and sometimes wheat can be used to make sandwiches", "value": 800})
update_product(1, {"description": "A product made of flour and sometimes wheat can be used to make sandwiches", "value": 800})
update_product(1, {})
user_data['auth_header']["Authorization"] = "Bearer somethingsomething"
update_product(1, {})
get_products()
get_product(1)
signin({"username": "John", "password": "test1234"})
get_products()
get_product(1)
delete_product(0)
delete_product(1)
delete_product(2)
get_products()
get_product(1)
get_product_count()
logout()
logout()

signin({"username": "Katie", "password": "generationalgifts2019"})
get_products()
update_product(1, {"value": 19})
update_product(5, {"value": 19})
get_product(5)
get_product_count()
delete_product(5)
delete_product(5)
get_products()
get_product_count()
logout()

signin({"username": "Max", "password": "petroleumjelly1981"})
get_products()
update_product(5, {})
update_product(10, {"description": "Just wine cake!"})
get_product(10)
get_product_count()
delete_product(10)
delete_product(10)
get_products()
get_product_count()
logout()

signin({"username": "Alex", "password": "alexis1934"})
get_products()
update_product(11, {})
update_product(15, {"value": 1000})
get_product(15)
delete_product(15)
delete_product(15)
get_products()
get_product_count()
logout()
logout()

modified_user = users_list[0].copy()
modified_user["username"] = "Joshua"
modified_user["password_confirmation"] += "!"
signup(modified_user)
logout()
get_product_count()

modified_user["password_confirmation"] = modified_user["password_confirmation"][:-1]
signup(modified_user)
get_products()
get_product(0)

signin({"username": "Joshua", "password": "test1234"})
get_products()
get_product(0)
get_product_count()

user_data['auth_header']["Authorization"] = "Bearer fake fake"
get_product_count()
logout()
logout()
