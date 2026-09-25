import requests

api_url = "http://localhost:8000/api/v11"
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
    r = requests.get("http://localhost:8000/")
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

def get_available_books():
    print(f"[ * ] Getting available books...")
    r = requests.get(f"{api_url}/books/available",
        headers=user_data["auth_header"])
    print(r.text)
    print()

def get_unavailable_books():
    print(f"[ * ] Getting unavailable books...")
    r = requests.get(f"{api_url}/books/unavailable",
        headers=user_data["auth_header"])
    print(r.text)
    print()

def get_statistics():
    print(f"[ * ] Getting statistics...")
    r = requests.get(f"{api_url}/books/stats",
        headers=user_data["auth_header"])
    print(r.text)
    print()

def get_latest():
    print(f"[ * ] Getting latest...")
    r = requests.get(f"{api_url}/books/latest",
        headers=user_data["auth_header"])
    print(r.text)
    print()

def get_counts():
    print(f"[ * ] Getting counts...")
    r = requests.get(f"{api_url}/books/count",
        headers=user_data["auth_header"])
    print(r.text)
    print()

def get_all_books():
    print("[ * ] Getting all books...")
    r = requests.get(f"{api_url}/books/all", headers=user_data["auth_header"])
    print(r.text)
    print()

def get_own_books():
    print("[ * ] Getting own books...")
    r = requests.get(f"{api_url}/books", headers=user_data["auth_header"])
    print(r.text)
    print()

def get_book_by_id(book_id):
    print(f"[ * ] Getting book by id {book_id}...")
    r = requests.get(f"{api_url}/books/{book_id}", headers=user_data["auth_header"])
    print(r.text)
    print()

def update_book_by_id(book_id, book_details):
    print(f"Updating book by id {book_id}...")
    r = requests.put(f"{api_url}/books/{book_id}",
        json=book_details, headers=user_data["auth_header"])
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

def restore_book(book_id):
    print(f"[ * ] Restoring book with id {book_id}...")
    r = requests.post(f"{api_url}/books/{book_id}/restore", headers=user_data["auth_header"])
    print(r.text)
    print()


def create_book_for_user(book_details):
    print(f"[ * ] Creating book from account {user_data['username']} for user with id {book_details['user_id']}")
    r = requests.post(f"{api_url}/books", json=book_details,
        headers=user_data['auth_header'])
    print(r.text)
    print()

def delete_book_by_id(book_id):
    print(f"Deleting book by id {book_id}...")
    r = requests.delete(f"{api_url}/books/{book_id}", headers=user_data["auth_header"])
    print(r.text)
    print()

def get_books(author=None, title=None, year=None,
    available=None, pages=None, min_pages=None,
    max_pages=None, sort_by=None, order=None,
    limit=None, offset=None):
    print("[ * ] Getting books...")
    search_filters = {}
    if author:
        print(f"Searching by author: {author}")
        search_filters["author"] = author

    if title:
        print(f"Searching by title: {title}")
        search_filters["title"] = title

    if year:
        print(f"Searching by year: {year}")
        search_filters["year"] = year

    if available is not None:
        print(f"Searching by availability: {available}")
        search_filters["available"] = available

    if pages:
        print(f"Searching by pages: {pages}")
        search_filters["pages"] = pages

    if min_pages:
        print(f"Searching by minimum pages: {min_pages}")
        search_filters["min_pages"] = min_pages

    if max_pages:
        print(f"Searching by maximum pages: {max_pages}")
        search_filters["max_pages"] = max_pages
    if sort_by:
        print(f"Searching by sort type: {sort_by}")
        search_filters["sort_by"] = sort_by
        if order:
            print(f"Searching by order type: {order}")
            search_filters["order"] = order

    if limit:
        print(f"Searching by pagination limit: {limit}")
        search_filters["limit"] = limit

    if offset:
        print(f"Searching by pagination offset: {offset}")
        search_filters["offset"] = offset

    r = requests.get(f"{api_url}/books", params=search_filters, headers=user_data['auth_header'])
    print(r.text)
    print()

check_api_status()
signup(
    {
        "username": "Depinjector21",
        "fullname": "Dependency Injector",
        "password": "Depinjector1981",
        "password_confirmation": "Depinjector1981"
    }
)

signin({"username": "Depinjector21", "password": "Depinjector1981"})
get_all_books()
delete_book_by_id(44)
update_user_role(2, "admin")
get_user(2)
get_users()
get_book_by_id(40)
signout()

signin({"username": "John", "password": "test1234"})

get_all_books()
delete_book_by_id(44)
update_user_role(3, "admin")
get_user(3)
get_users()
get_book_by_id(40)
signout()

signin({"username": "Katie", "password": "generationalgifts2019"})
get_all_books()
delete_book_by_id(45)
delete_book_by_id(46)
update_user_role(1, "librarian")
get_user(1)
get_users()
get_book_by_id(40)

original_token = user_data["access_token"]
new_auth_header("rubbish token")
get_own_books()

new_auth_header("")
get_own_books()
new_auth_header(original_token)
update_book_by_id(13, {"year": 1988})
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
restore_book(45)
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
get_latest()
get_available_books()
get_unavailable_books()
get_statistics()
get_counts()
get_books(author="Gerry Conway")
get_books(title="Maximum Carnage")
get_books(year=1973,
    author="Gerry Conway"
)
get_books(year=1973,
    author="Gerry Conway",
    min_pages=80
)
get_books(year=1973,
    max_pages=300
)
get_books(year=1973,
    pages=120
)
get_books(year=1973,
    pages=122
)
get_books(title="The Princess Bride",
    author="William Goldman",
    year=1973
)
get_books(year=1973)
get_books(title="The Night Gwen Stacy Died",
    year=1973,
    author="Gerry Conway"
)
signout()
