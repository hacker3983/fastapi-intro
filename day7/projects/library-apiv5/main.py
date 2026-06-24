import os
import json
from fastapi import FastAPI, HTTPException, status, Query, Depends
from models.models import *
from library_db import *
from typing import Annotated

app = FastAPI()

def get_library_db():
    db_instance = LibraryDB()
    try:
        yield db_instance
    finally:
        db_instance.close_db()

Library = Annotated[LibraryDB, Depends(get_library_db)]

def new_book_model(book_details: BookCreateRequest, my_library: Library):
    new_book = my_library.add_book(book_details)
    return new_book

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
def create_book(book_details: BookCreateRequest, my_library: Library):
    book = new_book_model(book_details, my_library)
    response = BookCreationResponse(
        data=book
    )
    return response

@app.get("/books/count",
    summary="Get book count",
    description="Retrieve total number of books in the library",
    response_model=BookCountResponse)
def get_books_count(my_library: Library):
    return BookCountResponse(
            data=my_library.get_book_count()
    )

@app.get("/books/latest",
    summary="Get the latest book",
    description="Retrieves the latest year book in the library",
    response_model=BookLatestResponse)
def get_latest_book(my_library: Library):
    return BookLatestResponse(
        data=my_library.get_latest_book()
    )

@app.get("/books/available",
    summary="Get available books",
    description="Retrieves books that are available in the library",
    response_model=BookAvailableResponse)
def get_available_books(my_library: Library):
    available_books = my_library.get_available_books()
    return BookAvailableResponse(
        data=available_books
    )

@app.get("/books/unavailable",
    summary="Get unavailable books",
    description="Retrieves books that are unavailable in the library",
    response_model=BookUnavailableResponse)
def get_unavailable_books(my_library: Library):
    unavailable_books = my_library.get_unavailable_books()
    return BookUnavailableResponse(
        data=unavailable_books
    )

@app.get("/books/stats", response_model=BookStatisticsResponse)
def get_books_statistics(my_library: Library):
    book_stats = my_library.get_book_stats()
    return BookStatisticsResponse(
            Total_books=book_stats["total_books"],
            Available_books=book_stats["available_books"],
            Unavailable_books=book_stats["unavailable_books"]
    )

@app.post("/books/import", response_model=BookImportResponse,
    responses={400: {"model": ErrorResponse}})
def import_books(book_details: BookImportRequest, my_library: Library):
    book = None
    errors = []
    import_count = 0
    detail_list = book_details.books
    for book_detail in detail_list:
        book = new_book_model(book_detail, my_library)
        if book is None:
            errors.append(book_detail)
            continue
        import_count += 1
    if errors:
        book_creation_error(errors=errors, import_count=import_count)
    return BookImportResponse(data=book_details.books)

@app.get("/books/export")
def export_books(my_library: Library):
    return {"Books": my_library.get_books()}

@app.get("/books",
    summary="Get all books",
    description="Retrieves all books in the library or based on search filters author, title, year, available, pages, min pages, max pages, and sort by title, pages, year and order",
    responses={404: {"model": ErrorResponse}}
    )
def get_books(author: str | None = None, title: str | None = None,
    year: int | None = None, available: bool | None = None, pages: int | None = None,
    min_pages: int | None = None, max_pages: int | None = None, sort_by: str | None = None,
    order:str | None = None, limit: int | None = Query(default=None, gt=0),
    offset: int = Query(default=0, ge=0), my_library: Library = Library):
    results = my_library.filter_books(author, title, year, available, pages, min_pages, max_pages,
            sort_by, order, limit, offset)
    if not results:
        book_not_found_error()
    results = {"Books": results}
    return results

@app.get("/books/{book_id}",
    summary="Get book by id",
    description="Retrieves a book by it's id from the library",
    response_model=BookResponse,
    responses={404: {"model": ErrorResponse}})
def get_book_by_id(book_id: int, my_library: Library):
    result = my_library.get_book_by_id(book_id)
    if not result:
        book_not_found_error(book_id)
    return result

@app.put("/books/{book_id}",
    summary="Update book by id",
    description="Updates the details of a book within library by it's id",
    response_model=BookUpdatedResponse,
    responses={404: {"model": ErrorResponse}}
    )
def update_book_by_id(book_id: int, book_details: BookUpdateRequest,
    my_library: Library):
    book = my_library.update_book(book_id, book_details)
    if not book:
        book_not_found_error(book_id)
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
def delete_book_by_id(book_id: int, my_library: Library):
    deleted_book = my_library.remove_book(book_id)
    if not deleted_book:
        book_not_found_error(book_id)
    response = BookDeletionResponse(
        data=deleted_book
    )
    return response
