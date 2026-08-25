import requests

api_url = "http://localhost:8000"
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
    print("[ * ] Checking API Status...")
    r = requests.get(api_url)
    print(r.text)
    print()

def signup(user_detail):
    print(f"[ * ] Signing up as user {user_detail['username']}...")
    r = requests.post(f"{api_url}/signup", json=user_detail)
    print(r.text)
    print()

def signin(user_details):
    print(f"[ * ] Signing into user {user_details['username']}...")
    r = requests.post(f"{api_url}/signin",
        data=user_details)
    print(r.text)
    print()
    if r.status_code == 200:
        response = r.json()
        user_data["username"] = user_details["username"]
        user_data["access_token"] = response["access_token"]
        user_data["logged_in"] = True
        new_auth_header(response["access_token"])

def signout():
    if user_data["logged_in"]:
        print(f"[ * ] Signing out of user {user_data['username']}...")
        user_data["username"] = None
        user_data["logged_in"] = False
        user_data["access_token"] = None
        user_data["auth_header"] = None
        return
    print("[ * ] Not signed in...")

def get_all_books():
    print("[ * ] Getting all books...")
    r = requests.get(f"{api_url}/books/all", headers=user_data["auth_header"])
    print(r.text)
    print()

def get_book_by_id(book_id):
    print(f"[ * ] Getting book by id {book_id}...")
    r = requests.get(f"{api_url}/books/{book_id}", headers=user_data["auth_header"])
    print(r.text)
    print()

def get_own_books():
    print("[ * ] Getting own books...")
    r = requests.get(f"{api_url}/books", headers=user_data["auth_header"])
    print(r.text)
    print()

def restore_book(book_id):
    print(f"[ * ] Restoring book with id {book_id}...")
    r = requests.post(f"{api_url}/books/{book_id}/restore", headers=user_data["auth_header"])
    print(r.text)
    print()

def update_book_by_id(book_id, book_details):
    print(f"Updating book by id {book_id}...")
    r = requests.put(f"{api_url}/books/{book_id}",
        json=book_details, headers=user_data["auth_header"])
    print(r.text)
    print()

def delete_book_by_id(book_id):
    print(f"Deleting book by id {book_id}...")
    r = requests.delete(f"{api_url}/books/{book_id}", headers=user_data["auth_header"])
    print(r.text)
    print()

def create_book_for_user(book_details):
    print(f"[ * ] Creating book from account {user_data['username']} for user with id {book_details['user_id']}")
    r = requests.post(f"{api_url}/books", json=book_details,
        headers=user_data['auth_header'])
    print(r.text)
    print()

def import_books(books):
    print("[ * ] Importing books...")
    r = requests.post(f"{api_url}/books/import",
        json={"books": books},
        headers=user_data['auth_header']
    )
    print(r.text)
    print()

def export_books():
    print("[ * ] Exporting books...")
    r = requests.get(f"{api_url}/books/export", headers=user_data['auth_header'])
    print(r.text)
    print()

def get_user(user_id):
    print(f"[ * ] Getting user by id {user_id}...")
    r = requests.get(f"{api_url}/users/{user_id}",
        headers=user_data["auth_header"])
    print(r.text)
    print()

def get_users():
    print("[ * ] Getting users...")
    r = requests.get(f"{api_url}/users", headers=user_data["auth_header"])
    print(r.text)
    print()

def update_user_role(user_id, role):
    print(f"[ * ] Updating role for user with id {user_id}...")
    r = requests.patch(f"{api_url}/users/{user_id}/role",
        headers=user_data["auth_header"], params={"role": role})
    print(r.text)
    print()

check_api_status()
user_details = {
    "username": "Anonymous",
    "fullname": "Anonymous User",
    "password": "test1234",
    "password_confirmation": "test1234"
} 
signup(user_details)
signin({"username": "John", "password": "test1234"})
get_all_books()
restore_book(7)
restore_book(37)
restore_book(31)
signout()
signin({"username": "Katie", "password": "generationalgifts2019"})
get_all_books()
restore_book(29)
signout()
signin({"username": "Max", "password": "petroleumjelly1981"})
restore_book(27)
get_all_books()
get_own_books()
get_book_by_id(13)
update_book_by_id(27, {"author": "Just some random author lol"})
delete_book_by_id(27)
update_book_by_id(13, {"year": 1988})
create_book_for_user(
    {
        "title": "The little mermaid",
        "author": "Gerry Conway",
        "year": 1973,
        "pages": 122,
        "available": True,
        "user_id": 4
    }
)
get_own_books()

import_books(
    [{
        "title": "The little mermaid",
        "author": "Gerry Conway",
        "year": 1973,
        "pages": 122,
        "available": True,
        "user_id": 4
    }]
)
export_books()
get_users()
update_user_role(1, "user")
get_user(1)
signout()

signin({"username": "John", "password": "test1234"})
update_book_by_id(13, {"year": 1973})
get_book_by_id(13)
get_all_books()
create_book_for_user(
    {
        "title": "The little mermaid",
        "author": "Gerry Conway",
        "year": 1973,
        "pages": 122,
        "available": True,
        "user_id": 3
    }
)
import_books(
    [{
        "title": "The little mermaid",
        "author": "Gerry Conway",
        "year": 1973,
        "pages": 122,
        "available": True,
        "user_id": 3
    }]
)
export_books()
get_users()
update_user_role(5, "admin")
get_users()
update_user_role(5, "librarian")
update_user_role(5, "rubbish")
get_users()
get_user(1)
get_user(5)
get_user(4)
signout()

signin({"username": "Katie", "password": "generationalgifts2019"})
delete_book_by_id(13)
get_book_by_id(13)
get_all_books()
restore_book(13)
get_book_by_id(13)
create_book_for_user(
{
    "title": "The little mermaid",
    "author": "Gerry Conway",
    "year": 1973,
    "pages": 122,
    "available": True,
    "user_id": 4
})

import_books(
    [{
        "title": "The little mermaid",
        "author": "Gerry Conway",
        "year": 1973,
        "pages": 122,
        "available": True,
        "user_id": 4
    }]
)
export_books()
get_users()
update_user_role(1, "user")
get_user(3)

original_token = user_data['auth_header']
print("[ * ] Testing invalid token error...")
new_auth_header("fffffff")
get_own_books()
get_all_books()

print("[ * ] Testing missing token error...")
new_auth_header("")
get_own_books()
get_all_books()
print()

print("[ * ] Restoring original token...")
new_auth_header(original_token)
print()

signout()
