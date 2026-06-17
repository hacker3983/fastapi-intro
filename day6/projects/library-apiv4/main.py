import os
import json
from fastapi import FastAPI, HTTPException, status, Query
from models.models import *

def deserialize_json_to_response(loaded_books):
    my_books = loaded_books["Books"]
    id_counter = loaded_books["BOOK_ID_COUNTER"]
    result:list[BookResponse] = []
    for book in my_books:
        book_response = BookResponse.model_validate(book)
        result.append(book_response)
    return (id_counter, result)

def serialize_books_to_json(my_books):
    serialized_list = []
    for i, book in enumerate(my_books):
        serialized_list.append(dict(book))
    serialized_output = json.dumps({"Books": serialized_list, "BOOK_ID_COUNTER": book_id_counter}, indent=4)
    return serialized_output

def load_books():
    global books, book_id_counter
    if not os.path.isfile("books.json") and not os.path.isfile("backups.json"):
        return False
    json_file = "books.json"
    restored_backup = False
    if os.path.isfile("backups.json") and not os.path.isfile("books.json"):
        json_file = "backups.json"
        restored_backup = True
    with open(json_file) as f:
        loaded_books = json.loads(f.read())
        if not loaded_books:
            return False
        if not loaded_books["Books"]:
            return False
        result = deserialize_json_to_response(loaded_books)
        book_id_counter = result[0]
        books = result[1]
    if restored_backup:
        print("Successfully loaded and restored books from backup...")
        save_books()
    else:
        print("Successfully loaded books...")
    return True

def save_books():
    with open("books.json", "w") as f:
        json_data = serialize_books_to_json(books)
        f.write(json_data)
        with open("backups.json", "w") as backup_file:
            backup_file.write(json_data)
        print("Successfully saved data!")

books:list[BookResponse] = []
book_id_counter = 0
load_books()

app = FastAPI()
def new_book_model(book_details: BookCreateRequest):
    global book_id_counter
    try:
        new_book = BookResponse(
            id = book_id_counter + 1,
            title = book_details.title,
            author = book_details.author,
            year = book_details.year,
            pages = book_details.pages,
            available = True
        )
        book_id_counter += 1
    except:
        return None
    return new_book

def find_book_by_id(book_id):
    for i, book in enumerate(books):
        if book.id == book_id:
            return (i, book)
    return None

def filter_books(author=None, title=None, year=None,
    available=None, pages=None, min_pages=None, max_pages=None):
    results = books
    criteria_counter = 0
    if author:
        results = [book for book in results if book.author == author]
        if results:
            criteria_counter += 1

    if title:
        results = [book for book in results if book.title == title]
        if results:
            criteria_counter += 1

    if year:
        results = [book for book in results if book.year == year]
        if results:
            criteria_counter += 1

    if available is not None:
        results = [book for book in results if book.available == available]
        if results:
            criteria_counter += 1

    if pages:
        results = [book for book in results if book.pages == pages]
        if results:
            criteria_counter += 1

    if min_pages:
        results = [book for book in results if book.pages >= min_pages]
        if results:
            criteria_counter += 1

    if max_pages:
        results = [book for book in results if book.pages <= max_pages]
        if results:
            criteria_counter += 1
    
    return (criteria_counter, results)

def find_latest_book():
    latest_year = 0
    found = False
    for i, book in enumerate(books):
        current_latest = books[latest_year].year
        if book.year > current_latest:
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

def sort_error(option=None, order=None):
    raise HTTPException(
        status_code=400,
        detail=f"Invalid sort field from input ({option})."
    )

def sort_books(books, option=None, order=None):
    results = books
    has_sorted = False
    if not option:
        return results
    if option == "title":
        results = sorted(results, key=lambda book: book.title)
        has_sorted = True
    elif option == "pages":
        results = sorted(results, key=lambda book: book.pages)
        has_sorted = True
    elif option == "year":
        results = sorted(results, key=lambda book: book.year)
        has_sorted = True
    else:
        sort_error(option)
    if option and order and has_sorted and order.lower() == "desc":
        results = results[::-1]
    return results

def paginate_books(books, limit=None, offset=0):
    results = books
    if limit is None:
        return results
    return results[offset:offset + limit]

def book_not_found_error(book_id=None):
    detail = "The requested book was not found"
    if book_id:
        detail += f" with id {book_id}"
    detail += "!"
    raise HTTPException(
            status_code=404,
            detail=detail
          )

def book_creation_error(book_detail=None, errors=None, import_count=None):
    detail = "The requested book"
    if errors:
        detail += "s could not be created:\n"
    if book_detail:
        detail += f"{book_detail} could not be created!"
    elif errors:
        detail += f"{errors}\n"
    if import_count:
        detail += f"\nImported {import_count}."
    raise HTTPException(
            status_code=400,
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
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": ErrorResponse}})
def create_book(book_details: BookCreateRequest):
    book = new_book_model(book_details)
    if book is None:
        book_creation_error()
    books.append(book) 
    response = BookCreationResponse(
        data=book
    )
    save_books()
    return response

@app.get("/books/count",
    summary="Get book count",
    description="Retrieve total number of books in the library",
    response_model=BookCountResponse)
def get_books_count():
    return BookCountResponse(
            data=len(books)
    )

@app.get("/books/latest",
    summary="Get the latest book",
    description="Retrieves the latest year book in the library",
    response_model=BookLatestResponse)
def get_latest_book():
    result = find_latest_book()
    book = None
    if result:
        book = result[1]
    return BookLatestResponse(
        data=book
    )

@app.get("/books/available",
    summary="Get available books",
    description="Retrieves books that are available in the library",
    response_model=BookAvailableResponse)
def get_available_books():
    available_books = filter_books(available=True)[1]
    return BookAvailableResponse(
        data=available_books
    )

@app.get("/books/unavailable",
    summary="Get unavailable books",
    description="Retrieves books that are unavailable in the library",
    response_model=BookUnavailableResponse)
def get_unavailable_books():
    unavailable_books = filter_books(available=False)[1]
    return BookUnavailableResponse(
        data=unavailable_books
    )

@app.get("/books/stats", response_model=BookStatisticsResponse)
def get_books_statistics():
    total_books = len(books)
    available_books = get_available_books()
    available_books_count = len(available_books.data)
    return BookStatisticsResponse(
            Total_books=total_books,
            Available_books=available_books_count,
            Unavailable_books=total_books - available_books_count
    )

@app.post("/books/import", response_model=BookImportResponse,
    responses={400: {"model": ErrorResponse}})
def import_books(book_details: BookImportRequest):
    book = None
    errors = []
    import_count = 0
    detail_list = book_details.books
    for book_detail in detail_list:
        book = new_book_model(book_detail)
        if book is None:
            errors.append(book_detail)
            continue
        books.append(book)
        import_count += 1
    save_books()
    if errors:
        book_creation_error(errors=errors, import_count=import_count)
    return BookImportResponse(data=book_details.books)

@app.get("/books/export")
def export_books():
    return {"Books": books}

@app.get("/books",
    summary="Get all books",
    description="Retrieves all books in the library or based on search filters author, title, year, available, pages, min pages, max pages, and sort by title, pages, year and order",
    responses={404: {"model": ErrorResponse}}
    )
def get_books(author: str | None = None, title: str | None = None,
    year: int | None = None, available: bool | None = None, pages: int | None = None,
    min_pages: int | None = None, max_pages: int | None = None, sort_by: str | None = None,
    order:str | None = None, limit: int | None = Query(default=None, gt=0),
    offset: int = Query(default=0, ge=0)):
    criteria_count = get_criteria_count(author, title, year,
        available, pages, min_pages, max_pages)
    criteria_counter, results = filter_books(author, title, year,
        available, pages, min_pages, max_pages)
    if criteria_counter != criteria_count:
        book_not_found_error()
    results = sort_books(results, sort_by, order)
    results = paginate_books(results, limit, offset)
    results = {"Books": results}
    return results

@app.get("/books/{book_id}",
    summary="Get book by id",
    description="Retrieves a book by it's id from the library",
    response_model=BookResponse,
    responses={404: {"model": ErrorResponse}})
def get_book_by_id(book_id: int):
    result = find_book_by_id(book_id)
    if not result:
        book_not_found_error(book_id)
    book = result[1]
    return book

@app.put("/books/{book_id}",
    summary="Update book by id",
    description="Updates the details of a book within library by it's id",
    response_model=BookUpdatedResponse,
    responses={404: {"model": ErrorResponse}}
    )
def update_book_by_id(book_id: int, book_details: BookUpdateRequest):
    result = find_book_by_id(book_id)
    if not result:
        book_not_found_error(book_id)
    book = result[1]
    updated = False
    if book_details.title:
        book.title = book_details.title
        updated = True
    if book_details.author:
        book.author = book_details.author
        updated = True
    if book_details.year:
        book.year = book_details.year
        updated = True
    if book_details.pages:
        book.pages = book_details.pages
        updated = True
    if book_details.available is not None:
        book.available = book_details.available
        updated = True
    if updated:
        save_books()
    response = BookUpdatedResponse(
        data=book
    )
    return response

@app.delete("/books/{book_id}",
    summary="Remove a book",
    description="Removes a book by it's id from the library",
    response_model=BookDeletionResponse,
    responses={
        404: {"model": ErrorResponse}
    })
def delete_book_by_id(book_id: int):
    result = find_book_by_id(book_id)
    if not result:
        book_not_found_error(book_id)
    book = result[1]
    response = BookDeletionResponse(
        data=book
    )
    book_index = result[0]
    books.pop(book_index)
    save_books()
    return response
