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

def signup(user_detail):
    print(f"[ * ] Signing up as user {user_detail['username']}...")
    r = requests.post(f"{api_url}/signup", json=user_detail)
    print(r.text)
    print()

def create_accounts(users_list):
    for user_details in users_list:
        user_details["password_confirmation"] = user_details["password"]
        signup(user_details)

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

def create_books(books):
    for book in books:
        create_book(book)

def create_book_raw(book):
    title = book if not book.get("title") else book["title"]
    print(f"[ * ] Creating raw book {title}...")
    r = requests.post(f"{api_url}/books",
        json=book, headers=user_data['auth_header'])
    print(r.text)
    print()

def create_books_raw(books):
    for book in books:
        create_book_raw(book)

def create_books_for_users(users_list, books_list):
    for i, user in enumerate(users_list):
        username = user['username']
        password = user['password']
        print(f"[ * ] Signing into user {username} to create books...")
        signin({"username": username, "password": password})
        books = books_list[username]
        create_books_raw(books)

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

users_list = [
    {
        "username": "John",
        "fullname": "John Doe",
        "password": "test1234"
    },
    {
        "username": "Katie",
        "fullname": "Katie Williams",
        "password": "generationalgifts2019"
    },
    {
        "username": "Max",
        "fullname": "Max Carter",
        "password": "petroleumjelly1981"
    },
    {
        "username": "Alex",
        "fullname": "Alex Doe",
        "password": "alexis1934"
    }
]

books_list = {
    "John": [
        {
            "title": "The Night Gwen Stacy Died",
            "author": "Gerry Conway",
            "year": 1973,
            "pages": 122,
            "available": True
        },
        {
            "title": "Maximum Carnage",
            "author": "Tom DeFalco",
            "year": 1994,
            "pages": 150,
            "available": False
        },
        {
            "title": "The Princess Bride",
            "author": "William Goldman",
            "year": 1973,
            "pages": 142,
            "available": True
        },
        {
            "title": "Detective Comics",
            "author": "Bill Finger",
            "year": 1939,
            "pages": 200,
            "available": False
        },
        {
            "title": "The Night Gwen Stacy Died",
            "author": "Gerry Conway",
            "year": 1973,
            "pages": 122,
            "available": True
        },
        {
            "title": "",
            "author": "",
            "year": 0,
            "pages": 0,
            "available": False
        }
    ],
    "Katie": [
        {
            "title": "The Amazing spiderman",
            "author": "Some made up stuff",
            "year": 1989,
            "pages": 150,
            "available": True
        },
        {
            "title": "Superman",
            "author": "Tom DeFalco",
            "year": 2005,
            "pages": 149,
            "available": False
        },
        {
            "title": "The Justice League",
            "author": "William Goldman",
            "year": 2025,
            "pages": 189,
            "available": True
        },
        {
            "title": "Python Programming",
            "author": "Bill Finger",
            "year": 1939,
            "pages": 305,
            "available": False
        },
        {
            "title": "C++ Programming",
            "author": "Bjarne Strostroupe lol",
            "year": 1973,
            "pages": 122,
            "available": True
        },
        {
            "title": "",
            "author": "",
            "year": 0,
            "pages": 0,
            "available": False
        }
    ],
    "Max": [
        {
            "title": "C programming",
            "author": "Denis Ritchie",
            "year": 1973,
            "pages": 122,
            "available": True
        },
        {
            "title": "Functional Programming",
            "author": "I don't know!",
            "year": 1994,
            "pages": 150,
            "available": False
        },
        {
            "title": "The Networking Protocol",
            "author": "William Goldman",
            "year": 1973,
            "pages": 142,
            "available": True
        },
        {
            "title": "Some random stuff",
            "author": "Bill Finger",
            "year": 1939,
            "pages": 200,
            "available": False
        },
        {
            "title": "The Tom and Jerry",
            "author": "Gerry Conway",
            "year": 1973,
            "pages": 122,
            "available": True
        },
        {
            "title": "",
            "author": "",
            "year": 0,
            "pages": 0,
            "available": False
        }
    ],
    "Alex": [
        {
            "title": "The little mermaid",
            "author": "Gerry Conway",
            "year": 1973,
            "pages": 122,
            "available": True
        },
        {
            "title": "Sea Whales",
            "author": "Tom DeFalco",
            "year": 1994,
            "pages": 150,
            "available": False
        },
        {
            "title": "The great white shark",
            "author": "William Goldman",
            "year": 1973,
            "pages": 142,
            "available": True
        },
        {
            "title": "The skateboard",
            "author": "Bill Finger",
            "year": 1939,
            "pages": 200,
            "available": False
        },
        {
            "title": "The darknight",
            "author": "Gerry Conway",
            "year": 1973,
            "pages": 122,
            "available": True
        },
        {
            "title": "",
            "author": "",
            "year": 0,
            "pages": 0,
            "available": False
        }
    ]
}

check_api_status()
create_accounts(users_list)
create_books_for_users(users_list, books_list)
signin({"username": "John", "password": "test1234"})
signin({"username": "John", "password": "wrongpassword"})
signin({"username": "Alex", "password": "invaliduser1234"})
user_data['auth_header']["Authorization"] = "Bearer somethingsomething"
get_books()
signin({"username": "John", "password": "test1234"})
username = user_data["username"]
get_books()
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
update_book_by_id(3, books_list[username][3])
update_book_by_id(4, books_list[username][2])
get_books_count()
get_books()
get_book_by_id(3)
get_book_by_id(4)
get_books(available=True)
get_books(available=False)
get_available_books()
update_book_by_id(3, {
    "year": 0,
    "pages": 0,
    "title": "",
    "author": ""
    }
)
get_books(author="Someone")
get_latest_book()
update_book_by_id(2, books_list[username][1])
get_unavailable_books()

get_books(pages=200)

update_book_by_id(2, {
        "year": 2027,
        "author": "A" * 60,
        "title": "A" * 120,
        "pages": 0
    }
)

delete_book_by_id(3)
delete_book_by_id(4)
get_books_count()
get_latest_book()
get_available_books()
get_books_statistics()

get_book_by_id(3)
get_book_by_id(4)
get_books()
get_unavailable_books()
delete_book_by_id(5)
delete_book_by_id(1)

update_book_by_id(0, {
    "author": "John Doe"
})

update_book_by_id(1, {
    "author": "John Doe"
})

get_books_count()
get_latest_book()
get_available_books()
delete_book_by_id(2)
delete_book_by_id(0)
get_books_statistics()

get_books_count()
get_books()
get_latest_book()
get_unavailable_books()

create_books(books_list[username])
get_books(sort_by="title")
get_books(sort_by="title", order="desc")

get_books(sort_by="year")
get_books(sort_by="year", order="desc")

get_books(sort_by="pages")
get_books(sort_by="pages", order="desc")

get_books_statistics()

update_book_by_id(10, {"available": False})
update_book_by_id(7, {"available": False})

get_books_statistics()

get_books(sort_by="something great", order="ffjjf")

create_books(books_list[username])
create_books(books_list[username])
get_books_statistics()

get_books(limit=2)
get_books(limit=4, offset=2)
get_books(sort_by="year", limit=3, offset=4)
get_books(sort_by="year", order="desc", limit=6, offset=3)
get_books(limit=-100)
get_books(offset=-50)

create_books_raw([{"dummy book": "dummy test"}, {"dummy 1234": "something"}])
export_books()
import_books(books_list[username])
export_books()
import_request = books_list[username].copy()
import_request.append({"dummy book": "dummy test", "dummy 1234": "something"})
import_books(import_request)
export_books()

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
get_books_statistics()
signout()
signin({"username": "Katie", "password": "wrongpasssword bro!"})
get_books()
signout()

signin({"username": "Katie", "password": "generationalgifts2019"})
get_books()
update_book_by_id(1, {"title": "Changed the name bro!"})
update_book_by_id(21, {"title": "Changed the name!"})
update_book_by_id(6, {"year": 1994, "available": False})
get_books_statistics()
delete_book_by_id(6)
delete_book_by_id(6)
get_books()
get_books_statistics()
get_books(sort_by="year")
get_books(sort_by="year", order="desc")
get_books_statistics()
signout()

signin({"username": "Max", "password": "petroleumjelly1981"})
get_books()
get_books_statistics()
delete_book_by_id(8)
update_book_by_id(11, {"year": 1975, "available": False})
update_book_by_id(14, {"available": False})
get_books_statistics()
get_books(sort_by="author", limit=2)
get_books(sort_by="pages")
get_books(sort_by="pages", order="desc")
delete_book_by_id(11)
delete_book_by_id(12)
delete_book_by_id(14)
get_books()
get_books_statistics()
signout()

signin({"username": "Alex", "password": "alexis1934"})
get_books()
get_books_statistics()
get_books(sort_by="title", offset=2, limit=10)
delete_book_by_id(14)
delete_book_by_id(0)
delete_book_by_id(16)
delete_book_by_id(17)
delete_book_by_id(18)
delete_book_by_id(19)
get_books()
get_books_statistics()

users_listcopy = users_list.copy()
users_listcopy[0]["password"] = users_listcopy[0]["password"][:6]
users_listcopy[1]["password"] = users_listcopy[1]["password"][:6]
users_listcopy[1]["password_confirmation"] = users_listcopy[1]["password"][:6]
create_accounts(users_list)
signout()
signout()
