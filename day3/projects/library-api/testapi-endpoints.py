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

def get_books(author=None, title=None, year=None):
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
get_books(title="The Princess Bride",
    author="William Goldman",
    year=1973
)
get_books(year=1973)

update_book_by_id(3, books[3])
update_book_by_id(4, books[2])
get_books_count()
get_books()
get_book_by_id(3)
get_book_by_id(4)

get_books(author="Someone")
get_latest_book()

delete_book_by_id(3)
delete_book_by_id(4)
get_books_count()
get_latest_book()

get_book_by_id(3)
get_book_by_id(4)
get_books()

delete_book_by_id(5)
delete_book_by_id(1)
get_books_count()
get_latest_book()

delete_book_by_id(2)
delete_book_by_id(0)

get_books_count()
get_books()
get_latest_book()
