from fastapi import APIRouter, Depends, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from models import (
    BookRestorationResponse, BookCreationResponse, ErrorResponse,
    BookCreationRequest, BookCountResponse, BookLatestResponse,
    BookUpdateRequest,
    BookUpdatedResponse, BookDeletionResponse,
    BookAvailableResponse, BookUnavailableResponse, BookStatisticsResponse,
    BookImportRequest, BookImportResponse, BookResponse
)
from jwt.exceptions import InvalidTokenError
from dependencies import my_library, oauth2_scheme
from helpers import (
    invalid_restoration_error, invalid_token_error,
    book_creation_error, book_not_found_error,
    forbidden_access_error
)
from typing import Annotated

router = APIRouter()

def new_book_model(token, book_details: BookCreationRequest):
    new_book = my_library.add_book(token, book_details)
    return new_book

@router.post("/books/{book_id}/restore",
    summary="Restore a book",
    description="Restores a book that was deleted. only for admins and librarians",
    status_code=status.HTTP_201_CREATED,
    response_model=BookRestorationResponse)
def restore_book(token: Annotated[str, Depends(oauth2_scheme)], book_id: int):
    try:
        result = my_library.restore_book(token, book_id)
    except InvalidTokenError:
        invalid_token_error()
    if result == False:
        forbidden_access_error()
    elif result is None:
        invalid_restoration_error()
    response = BookRestorationResponse(
        data=result
    )
    return response

@router.post("/books",
    summary="Create a book",
    description="Creates a book or adds it to the library",
    response_model=BookCreationResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": ErrorResponse}})
def create_book(token: Annotated[str, Depends(oauth2_scheme)], book_details: BookCreationRequest):
    try:
        book = new_book_model(token, book_details)
    except InvalidTokenError:
        invalid_token_error()
    response = BookCreationResponse(
        data=book
    )
    return response

@router.get("/books/count",
    summary="Get book count",
    description="Retrieve total number of books in the library",
    response_model=BookCountResponse)
def get_books_count(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        result = my_library.get_book_count(token)
    except InvalidTokenError:
        invalid_token_error()
    return BookCountResponse(
            data=result
    )

@router.get("/books/latest",
    summary="Get the latest book",
    description="Retrieves the latest year book in the library",
    response_model=BookLatestResponse)
def get_latest_book(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        result = my_library.get_latest_book(token)
    except InvalidTokenError:
        invalid_token_error()
    return BookLatestResponse(
        data=result
    )

@router.get("/books/available",
    summary="Get available books",
    description="Retrieves books that are available in the library",
    response_model=BookAvailableResponse)
def get_available_books(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        available_books = my_library.get_available_books(token)
    except InvalidTokenError:
        invalid_token_error()
    return BookAvailableResponse(
        data=available_books
    )

@router.get("/books/unavailable",
    summary="Get unavailable books",
    description="Retrieves books that are unavailable in the library",
    response_model=BookUnavailableResponse)
def get_unavailable_books(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        unavailable_books = my_library.get_unavailable_books(token)
    except InvalidTokenError:
        invalid_token_error()
    return BookUnavailableResponse(
        data=unavailable_books
    )

@router.get("/books/stats", response_model=BookStatisticsResponse)
def get_books_statistics(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        book_stats = my_library.get_book_stats(token)
    except InvalidTokenError:
        invalid_token_error()
    return BookStatisticsResponse(
            total_books=book_stats["total_books"],
            available_books=book_stats["available_books"],
            unavailable_books=book_stats["unavailable_books"]
    )

@router.post("/books/import", response_model=BookImportResponse,
    responses={400: {"model": ErrorResponse}})
def import_books(token: Annotated[str, Depends(oauth2_scheme)], book_details: BookImportRequest):
    book = None
    errors = []
    import_count = 0
    detail_list = book_details.books
    response = []
    for book_detail in detail_list:
        try:
            book = new_book_model(token, book_detail)
            response.append(book)
        except InvalidTokenError:
            invalid_token_error()
        if book is None:
            errors.append(book_detail)
            continue
        import_count += 1
    if errors:
        book_creation_error(errors=errors, import_count=import_count)
    return BookImportResponse(data=response)

@router.get("/books/export")
def export_books(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        result = my_library.get_books(token)
    except InvalidTokenError:
        invalid_token_error()
    return {"Books": result}

@router.get("/books/all",
    summary="Get books for all users",
    description="Retrieves books for all users as long as the user has an admin or librarian role")
def get_all_books(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        results = my_library.get_books(token, all_books=True)
    except InvalidTokenError:
        invalid_token_error()
    if results == False:
        forbidden_access_error()
    return {"Books": results}

@router.get("/books",
    summary="Get all books",
    description="Retrieves all books in the library or based on search filters author, title, year, available, pages, min pages, max pages, and sort by title, pages, year and order",
    responses={404: {"model": ErrorResponse}}
)
def get_books(token: Annotated[str, Depends(oauth2_scheme)], author: str | None = None, title: str | None = None,
    year: int | None = None, available: bool | None = None, pages: int | None = None,
    min_pages: int | None = None, max_pages: int | None = None, sort_by: str | None = None,
    order:str | None = None, limit: int | None = Query(default=None, gt=0),
    offset: int = Query(default=0, ge=0)):
    try:
        results = my_library.filter_books(token, author, title, year, available, pages, min_pages, max_pages,
        sort_by, order, limit, offset)
    except InvalidTokenError:
        invalid_token_error()
    if not results:
        book_not_found_error()
    results = {"Books": results}
    return results

@router.get("/books/{book_id}",
    summary="Get book by id",
    description="Retrieves a book by it's id from the library",
    response_model=BookResponse,
    responses={404: {"model": ErrorResponse}})
def get_book_by_id(token: Annotated[str, Depends(oauth2_scheme)], book_id: int):
    try:
        result = my_library.get_book_by_id(token, book_id)
    except InvalidTokenError:
        invalid_token_error()
    if not result:
        book_not_found_error(book_id)
    return result

@router.put("/books/{book_id}",
    summary="Update book by id",
    description="Updates the details of a book within library by it's id",
    response_model=BookUpdatedResponse,
    responses={404: {"model": ErrorResponse}}
    )
def update_book_by_id(token: Annotated[str, Depends(oauth2_scheme)], book_id: int, book_details: BookUpdateRequest):
    try:
        book = my_library.update_book(token, book_id, book_details)
    except InvalidTokenError:
        invalid_token_error()
    if not book:
        book_not_found_error(book_id)
    response = BookUpdatedResponse(
        data=book
    )
    return response

@router.delete("/books/{book_id}",
    summary="Remove a book",
    description="Removes a book by it's id from the library",
    response_model=BookDeletionResponse,
    responses={
        404: {"model": ErrorResponse}
    })
def delete_book_by_id(token: Annotated[str, Depends(oauth2_scheme)], book_id: int):
    try:
        deleted_book = my_library.remove_book(token, book_id)
    except InvalidTokenError:
        invalid_token_error()
    if not deleted_book:
        book_not_found_error(book_id)
    response = BookDeletionResponse(
        data=deleted_book
    )
    return response
