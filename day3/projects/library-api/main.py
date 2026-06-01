from fastapi import FastAPI, HTTPException
from models import *

books = []
book_id_counter = 0

app = FastAPI()

def new_book_model(book_details: BookModel):
    global book_id_counter
    book_id_counter += 1
    new_book = {
            "id": book_id_counter,
            "title": book_details.title,
            "author": book_details.author,
            "year": book_details.year,
            "pages": book_details.pages
    }
    return new_book

def find_book_by_id(book_id):
    for i, book in enumerate(books):
        if book["id"] == book_id:
            return (i, book)
    return None

def find_books_by_author(author):
    results = []
    for i, book in enumerate(books):
        if book["author"] == author:
            results.append((i, book))
    return results

def find_books_by_title_filter_list(title, filter_list):
    if not filter_list:
        return None
    results = []
    for i in range(0, len(filter_list)):
        book_index = filter_list[i][0]
        book = filter_list[i][1]
        if book["title"] == title:
            results.append((book_index, book))
    return results

def find_books_by_title(title, filter_list=[]):
    results = []
    if filter_list:
        results = find_books_by_title_filter_list(title,
                filter_list)
    if results:
        return results
    for i, book in enumerate(books):
        if book["title"] == title:
            results.append((i, book))
    return results

def find_books_by_year_filter_list(year, filter_list):
    if not filter_list:
        return None
    results = []
    for i in range(0, len(filter_list)):
        book_index = filter_list[i][0]
        book = filter_list[i][1]
        if book["year"] == year:
            results.append((book_index, book))
    return results

def find_books_by_year(year, filter_list=[]):
    results = []
    if filter_list:
        results = find_books_by_year_filter_list(title,
                    filter_list)
    if results:
        return results
    for i, book in enumerate(books):
        if book["year"] == year:
            results.append((i, book))
    return results

def find_book_by_criterias(author, title, year):
    if not author:
        return None
    if not title:
        return None
    if not year:
        return None
    for i, book in enumerate(books):
        if book["author"] == author and
           book["title"] == title and
           book["year"] == year:
           return (i, book)
    return None

def populate_book_results(results):
    populated_results = []
    for result in results:
        book = result[1]
        populated_results.append(book)
    return populated_results

def book_not_found_error(book_id=None):
    detail = "The requested book was not found"
    if book_id:
        detail += f" with id {book_id}"
    raise HTTPException(
            status_code=404,
            detail=f"The requested book was not found with id {book_id}!"
          )

@app.get("/")
def home():
    return LibraryAPIStatus()


@app.post("/books")
def create_book(book_details: BookModel):
    book = new_book_model(book_details)
    books.append(book)
    response = BookCreationUpdateResponse(
        message="Book created",
        data=BookCreation.model_validate(book)
    )
    return response

@app.get("/books")
def get_books(author: str | None = None, title = str | None = None,
    year = int | None = None):
    results = []
    result = find_book_by_criterias(author, title, year)
    if result:
        book = result[1]
        return {"Books": book}

    if author:
        results = find_books_by_author(author, results)
    
    if title:
        results = find_books_by_title(title, results)
    
    if year:
        results = find_books_by_year(year, results)

    if results:
        populated_results = populate_book_results(results)
        return populated_results

    if any([author, title, year]) and not results:
        book_not_found_error()
    return {"Books": books}

@app.get("/books/{book_id}")
def get_book_by_id(book_id: int):
    result = find_book_by_id(book_id)
    if not result:
        book_not_found_error(book_id)
    book = result[1]
    return book

@app.put("/books/{book_id}")
def update_book_by_id(book_id: int, book_details: BookModel):
    result = find_book_by_id(book_id)
    if not result:
        book_not_found_error(book_id)
    book = result[1]
    book["title"] = book_details.title
    book["author"] = book_details.author
    book["year"] = book_details.year
    book["pages"] = book_details.pages
    return book
