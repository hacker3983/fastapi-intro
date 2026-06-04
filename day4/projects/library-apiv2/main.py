from fastapi import FastAPI, HTTPException, status
from models.models import * 

books = []
book_id_counter = 0

app = FastAPI()

def new_book_model(book_details: BookCreateRequest):
    global book_id_counter
    book_id_counter += 1
    new_book = {
            "id": book_id_counter,
            "title": book_details.title,
            "author": book_details.author,
            "year": book_details.year,
            "pages": book_details.pages,
            "available": True
    }
    return new_book

def find_book_by_id(book_id):
    for i, book in enumerate(books):
        if book["id"] == book_id:
            return (i, book)
    return None

def filter_books(author=None, title=None, year=None,
    available=None, pages=None, min_pages=None, max_pages=None):
    results = books
    criteria_counter = 0
    if author:
        results = [book for book in results if book["author"] == author]
        if results:
            criteria_counter += 1

    if title:
        results = [book for book in results if book["title"] == title]
        if results:
            criteria_counter += 1

    if year:
        results = [book for book in results if book["year"] == year]
        if results:
            criteria_counter += 1

    if available is not None:
        results = [book for book in results if book["available"] == available]
        if results:
            criteria_counter += 1

    if pages:
        results = [book for book in results if book["pages"] == pages]
        if results:
            criteria_counter += 1

    if min_pages:
        results = [book for book in results if book["pages"] >= min_pages]
        if results:
            criteria_counter += 1

    if max_pages:
        results = [book for book in results if book["pages"] <= max_pages]
        if results:
            criteria_counter += 1
    
    return (criteria_counter, results)

def find_latest_book():
    latest_year = 0
    found = False
    for i, book in enumerate(books):
        current_latest = books[latest_year]["year"]
        if book["year"] > current_latest:
            latest_year = i
            found = True
    if found or len(books) == 1:
        return (latest_year, books[latest_year])
    return None

def get_criteria_count(author=None, title=None, year=None,
    available=None, pages=None, min_pages=None,
    max_pages=None):
    criteria_count = 0
    if author:
        criteria_count += 1
    if title:
        criteria_count += 1
    if year:
        criteria_count += 1
    if available is not None:
        criteria_count += 1
    if pages:
        criteria_count += 1
    if min_pages:
        criteria_count += 1
    if max_pages:
        criteria_count += 1
    return criteria_count

def book_not_found_error(book_id=None):
    detail = "The requested book was not found"
    if book_id:
        detail += f" with id {book_id}"
    detail += "!"
    raise HTTPException(
            status_code=404,
            detail=detail
          )

@app.get("/", summary="Get API info",
    description="Retrieves information about the api such as status, version info, etc",
    response_model=LibraryAPIStatus)
def home():
    return LibraryAPIStatus()

@app.post("/books",
    summary="Create a book",
    description="Creates a book or adds it to the library",
    response_model=BookCreationResponse,
    status_code=status.HTTP_201_CREATED)
def create_book(book_details: BookCreateRequest):
    book = new_book_model(book_details)
    books.append(book)
    book_creation = BookResponse.model_validate(book)
    response = BookCreationResponse(
        data=BookResponse.model_validate(book)
    )
    return response

@app.get("/books/count",
    summary="Get book count",
    description="Retrieve total number of books in the library")
def get_books_count():
    return {"Book count": len(books)}

@app.get("/books/latest",
    summary="Get the latest book",
    description="Retrieves the latest year book in the library")
def get_latest_book():
    result = find_latest_book()
    book = None
    if result:
        book = result[1]
    return {"Latest book": book}

@app.get("/books/available",
    summary="Get available books",
    description="Retrieves books that are available in the library")
def get_available_books():
    available_books = filter_books(available=True)[1]
    return {"Available books": available_books}

@app.get("/books/unavailable",
    summary="Get unavailable books",
    description="Retrieves books that are unavailable in the library")
def get_unavailable_books():
    unavailable_books = filter_books(available=False)[1]
    return {"Unavailable books": unavailable_books}

@app.get("/books",
    summary="Get all books",
    description="Retrieves all books in the library or based on search filters author, title, year, available, pages, min pages, and max pages")
def get_books(author: str | None = None, title: str | None = None,
    year: int | None = None, available: bool | None = None, pages: int | None = None,
    min_pages: int | None = None, max_pages: int | None = None):
    criteria_count = get_criteria_count(author, title, year,
        available, pages, min_pages, max_pages)
    criteria_counter, results = filter_books(author, title, year,
        available, pages, min_pages, max_pages)
    if criteria_counter != criteria_count:
        book_not_found_error()
    results = {"Books": results}
    return results

@app.get("/books/{book_id}",
    summary="Get book by id",
    description="Retrieves a book by it's id from the library",
    response_model=BookResponse)
def get_book_by_id(book_id: int):
    result = find_book_by_id(book_id)
    if not result:
        book_not_found_error(book_id)
    book = result[1]
    return book

@app.put("/books/{book_id}",
    summary="Update book by id",
    description="Updates the details of a book within library by it's id",
    response_model=BookUpdatedResponse)
def update_book_by_id(book_id: int, book_details: BookUpdateRequest):
    result = find_book_by_id(book_id)
    if not result:
        book_not_found_error(book_id)
    book = result[1]
    if book_details.title:
        book["title"] = book_details.title
    if book_details.author:
        book["author"] = book_details.author
    if book_details.year:
        book["year"] = book_details.year
    if book_details.pages:
        book["pages"] = book_details.pages
    if book_details.available != None:
        book["available"] = book_details.available
    response = BookUpdatedResponse(
        data=BookResponse.model_validate(book)
    )
    return response

@app.delete("/books/{book_id}",
    summary="Remove a book",
    description="Removes a book by it's id from the library",
    response_model=BookDeletionResponse)
def delete_book_by_id(book_id: int):
    result = find_book_by_id(book_id)
    if not result:
        book_not_found_error(book_id)
    book = result[1]
    response = BookDeletionResponse(
        data=BookResponse.model_validate(book)
    )
    book_index = result[0]
    books.pop(book_index)
    return response
