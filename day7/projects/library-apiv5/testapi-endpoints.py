import requests

endpoint_url = "http://localhost:8000"

def check_api_stats():
    print("[ * ] Checking api status...")
    r = requests.get(endpoint_url)
    print(r.text)
    print("Response Code:", r.status_code)
    print()

def create_book(book):
    print(f"[ * ] Creating book {book['title']}...")
    r = requests.post(f"{endpoint_url}/books",
        json={
            "title": book["title"],
            "author": book["author"],
            "year": book["year"],
            "pages": book["pages"],
            "available": book["available"]
        }
    )
    print(r.text)
    print()

def create_books(books):
    for book in books:
        create_book(book)

def create_book_raw(book):
    print(f"[ * ] Creating raw book {book}...")
    r = requests.post(f"{endpoint_url}/books",
        json=book)
    print(r.text)
    print()

def create_books_raw(books):
    for book in books:
        create_book_raw(book)

def import_books(books):
    print("[ * ] Importing books...")
    r = requests.post(f"{endpoint_url}/books/import",
        json={"books": books}
    )
    print(r.text)
    print()

def export_books():
    print("[ * ] Exporting books...")
    r = requests.get(f"{endpoint_url}/books/export")
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

    r = requests.get(f"{endpoint_url}/books", params=search_filters)
    print(r.text)
    print()

def get_book_by_id(book_id):
    print(f"[ * ] Getting book by id {book_id}...")
    r = requests.get(f"{endpoint_url}/books/{book_id}")
    print(r.text)
    print()

def get_latest_book():
    print("[ * ] Getting latest book...")
    r = requests.get(f"{endpoint_url}/books/latest")
    print(r.text)
    print()

def get_books_count():
    print("[ * ] Getting book count...")
    r = requests.get(f"{endpoint_url}/books/count")
    print(r.text)
    print()

def get_available_books():
    print("[ * ] Getting available books...")
    r = requests.get(f"{endpoint_url}/books/available")
    print(r.text)
    print()

def get_unavailable_books():
    print("[ * ] Getting unavailable books...")
    r = requests.get(f"{endpoint_url}/books/unavailable")
    print(r.text)
    print()

def get_books_statistics():
    print("[ * ] Getting statistics for books...")
    r = requests.get(f"{endpoint_url}/books/stats")
    print(r.text)
    print()

def update_book_by_id(book_id, book_details):
    print(f"[ * ] Updating book by id {book_id}...")
    r = requests.put(f"{endpoint_url}/books/{book_id}",
            json=book_details)
    print(r.text)
    print()

def delete_book_by_id(book_id):
    print(f"[ * ] Deleting book by id {book_id}...")
    r = requests.delete(f"{endpoint_url}/books/{book_id}")
    print(r.text)
    print()

books = [
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
]

check_api_stats()
create_books(books)
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
update_book_by_id(3, books[3])
update_book_by_id(4, books[2])
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
update_book_by_id(2, books[1])
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

create_books(books)
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

create_books(books)
create_books(books)
get_books_statistics()

get_books(limit=2)
get_books(limit=4, offset=2)
get_books(sort_by="year", limit=3, offset=4)
get_books(sort_by="year", order="desc", limit=6, offset=3)
get_books(limit=-100)
get_books(offset=-50)

create_books_raw([{"dummy book": "dummy test"}, {"dummy 1234": "something"}])
export_books()
import_books(books)
export_books()
import_request = books.copy()
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
