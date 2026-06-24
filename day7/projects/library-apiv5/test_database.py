from library_db import *

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
    }
]

my_library = LibraryDB(file="test.db")

def add_books(books):
    for book in books:
        print(f"Adding book {book['title']}")
        my_library.add_book(
            BookCreateRequest(
                title=book["title"],
                author=book["author"],
                year=book["year"],
                pages=book["pages"],
            )
        )

add_books(books)
print("Before removal:")
print(my_library.get_books())
print("After Removal:")
print(my_library.remove_book(3))
print(my_library.get_books())
print(my_library.get_book_by_id(2))
print("Before Update:")
print(my_library.get_books())
my_library.update_book(2, BookUpdateRequest(title="Changed the name"))
my_library.update_book(2, BookUpdateRequest(author="Changed author name"))
my_library.update_book(2, BookUpdateRequest(year=2026))
my_library.update_book(2, BookUpdateRequest(pages=1337))
my_library.update_book(2, BookUpdateRequest(available=True))
print("After Update:")
print(my_library.get_books())
