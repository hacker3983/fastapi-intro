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
    return user_data['auth_header']

def check_api_status():
    print("[ * ] Checking API Status...")
    r = requests.get(api_url)
    print(r.text)
    print()

def signin(user_details):
    print(f"[ * ] Signing into user {user_details['username']}...")
    r = requests.post(f"{api_url}/signin",
        data=user_details
    )
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

def export_books():
    print("[ * ] Exporting books...")
    r = requests.get(f"{api_url}/books/export", headers=user_data['auth_header'])
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
    print(f"[ * ] Getting book by id {book_id}...")
    r = requests.get(f"{api_url}/books/{book_id}", headers=user_data['auth_header'])
    print(r.text)
    print()

def get_latest_book():
    print("[ * ] Getting latest book...")
    r = requests.get(f"{api_url}/books/latest", headers=user_data['auth_header'])
    print(r.text)
    print()

def get_books_count():
    print("[ * ] Getting book count...")
    r = requests.get(f"{api_url}/books/count", headers=user_data['auth_header'])
    print(r.text)
    print()

def get_available_books():
    print("[ * ] Getting available books...")
    r = requests.get(f"{api_url}/books/available", headers=user_data['auth_header'])
    print(r.text)
    print()

def get_unavailable_books():
    print("[ * ] Getting unavailable books...")
    r = requests.get(f"{api_url}/books/unavailable", headers=user_data['auth_header'])
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

def delete_book_by_id(book_id):
    print(f"[ * ] Deleting book by id {book_id}...")
    r = requests.delete(f"{api_url}/books/{book_id}", headers=user_data['auth_header'])
    print(r.text)
    print()

check_api_status()
signin({"username": "John", "password": "test1234"})
get_books()
delete_book_by_id(27)
delete_book_by_id(29)
delete_book_by_id(31)
delete_book_by_id(37)
get_books_count()

get_books()
get_book_by_id(21)
get_book_by_id(22)
get_books(available=True)
get_books(available=False)
get_available_books()
update_book_by_id(25, {
    "year": 0,
    "pages": 0,
    "title": "",
    "author": ""
    }
)
get_latest_book()
get_unavailable_books()

get_books(pages=200)

update_book_by_id(25, {
        "year": 2027,
        "author": "A" * 60,
        "title": "A" * 120,
        "pages": 0
    }
)

get_available_books()
get_books_statistics()
get_unavailable_books()

get_books(sort_by="title")
get_books(sort_by="title", order="desc")

get_books(sort_by="year")
get_books(sort_by="year", order="desc")

get_books(sort_by="pages")
get_books(sort_by="pages", order="desc")

get_books_statistics()
export_books()
get_books_statistics()
signout()

signin({"username": "Katie", "password": "generationalgifts2019"})
get_books()
delete_book_by_id(7)
delete_book_by_id(9)
get_books_statistics()
get_unavailable_books()
get_available_books()
signout()

signin({"username": "Max", "password": "petroleumjelly1981"})
get_books()
delete_book_by_id(7)
delete_book_by_id(9)
get_books_statistics()
get_unavailable_books()
get_available_books()
signout()

signin({"username": "Alex", "password": "alexis1934"})
get_books()
get_books_statistics()
get_unavailable_books()
get_available_books()
update_book_by_id(20, {"year": 2026})
signout()
