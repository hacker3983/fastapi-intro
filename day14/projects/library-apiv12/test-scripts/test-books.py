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

def create_book(book):
    print(f"[ * ] Creating book {book['title']}...")
    r = requests.post(f"{api_url}/books",
        json={
            "title": book["title"],
            "author": book["author"],
            "year": book["year"],
            "pages": book["pages"],
            "available": book["available"]
        },
        headers=user_data['auth_header']
    )
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

def get_book_by_id(book_id):
    print("[ * ] Getting books...")
    r = requests.get(f"{api_url}/books/{book_id}", headers=user_data["auth_header"])
    print(r.text)
    print()

def get_books_statistics():
    print("[ * ] Getting statistics for books...")
    r = requests.get(f"{api_url}/books/stats", headers=user_data['auth_header'])
    print(r.text)
    print()

def update_book_by_id(book_id, book_details):
    print(f"[ * ] Updating book by id {book_id}...")
    r = requests.put(f"{api_url}/books/{book_id}",
            json=book_details, headers=user_data['auth_header'])
    print(r.text)
    print()

def restore_book(book_id):
    print(f"[ * ] Restoring book with id {book_id}...")
    r = requests.post(f"{api_url}/books/{book_id}/restore", headers=user_data["auth_header"])
    print(r.text)
    print()

def delete_book_by_id(book_id):
    print(f"[ * ] Deleting book by id {book_id}...")
    r = requests.delete(f"{api_url}/books/{book_id}", headers=user_data['auth_header'])
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

signin("Newuser1981", "test1234")
book = {
    "title": "Test Book",
    "author": "Test Auther",
    "year": 2026,
    "pages": 50,
    "available": True
}
get_books()
create_book(book)
get_books()
update_book_by_id(72, {"year": 1973})
get_books()
delete_book_by_id(73)
get_books()
restore_book(73)
signout()

signin("Katie", "generationalgifts2019")
restore_book(73)
signout()

signin("Newuser1981", "test1234")
get_books()
signout()

signin("Katie", "generationalgifts2019")
get_books(author="Gerry Conway")
get_books(title="Maximum Carnage")
get_books(year=1973,
    author="Gerry Conway"
)
get_books(year=1973,
    author="Gerry Conway",
    min_pages=80
)
signout()

signin("John", "test1234")
get_books(sort_by="year")
get_books(sort_by="year", order="desc")

get_books(limit=2)
get_books(limit=4, offset=2)
get_books(sort_by="year", limit=3, offset=4)
get_books(sort_by="year", order="desc", limit=6, offset=3)
get_books(limit=-100)
get_books(offset=-50)
get_books_statistics()
signout()

signin("Newuser1981", "test1234")
import_request = [
    {
        "title": "The Princess Bride",
        "author": "William Goldman",
        "year": 1973,
        "pages": 142,
        "available": True
    },
    {
        "title": "The Princess Bride",
        "author": "William Goldman",
        "year": 1973,
        "pages": 142,
        "available": True
    }
]
import_books(import_request)
export_books()
signout()
