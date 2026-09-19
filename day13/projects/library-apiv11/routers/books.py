from fastapi import APIRouter, Depends, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from services import books as books_service
from models import (
    BookRestorationResponse, BookCreationResponse, ErrorResponse,
    BookCreationRequest, BookCountResponse, BookLatestResponse,
    BookUpdateRequest,
    BookUpdatedResponse, BookDeletionResponse,
    BookAvailableResponse, BookUnavailableResponse, BookStatisticsResponse,
    BookImportRequest, BookImportResponse, BookResponse
)
from dependencies import oauth2_scheme, db_session
from typing import Annotated

router = APIRouter()

@router.post("/books/{book_id}/restore",
    summary="Restore a book",
    description="Restores a book that was deleted. only for admins and librarians",
    status_code=status.HTTP_201_CREATED,
    response_model=BookRestorationResponse)
def restore_book(token: Annotated[str, Depends(oauth2_scheme)], book_id: int, session: db_session):
    return books_service.restore_book(token, session, book_id)

@router.post("/books",
    summary="Create a book",
    description="Creates a book or adds it to the library",
    response_model=BookCreationResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": ErrorResponse}})
def create_book(token: Annotated[str, Depends(oauth2_scheme)], book_details: BookCreationRequest, session: db_session):
    return books_service.create_book(token, session, book_details)

@router.get("/books/count",
    summary="Get book count",
    description="Retrieve total number of books in the library",
    response_model=BookCountResponse)
def get_books_count(token: Annotated[str, Depends(oauth2_scheme)], session: db_session):
    return books_service.get_books_count(token, session)

@router.get("/books/latest",
    summary="Get the latest book",
    description="Retrieves the latest year book in the library",
    response_model=BookLatestResponse)
def get_latest_book(token: Annotated[str, Depends(oauth2_scheme)], session: db_session):
    return books_service.get_latest_book(token, session)

@router.get("/books/available",
    summary="Get available books",
    description="Retrieves books that are available in the library",
    response_model=BookAvailableResponse)
def get_available_books(token: Annotated[str, Depends(oauth2_scheme)], session: db_session):
    return books_service.get_available_books(token, session)

@router.get("/books/unavailable",
    summary="Get unavailable books",
    description="Retrieves books that are unavailable in the library",
    response_model=BookUnavailableResponse)
def get_unavailable_books(token: Annotated[str, Depends(oauth2_scheme)], session: db_session):
    return books_service.get_unavailable_books(token, session)

@router.get("/books/stats", response_model=BookStatisticsResponse)
def get_books_statistics(token: Annotated[str, Depends(oauth2_scheme)], session: db_session):
    return books_service.get_books_statistics(token, session)

@router.post("/books/import", response_model=BookImportResponse,
    responses={400: {"model": ErrorResponse}})
def import_books(token: Annotated[str, Depends(oauth2_scheme)], book_details: BookImportRequest, session: db_session):
    response = books_service.import_books(token, session, book_details)
    return response

@router.get("/books/export")
def export_books(token: Annotated[str, Depends(oauth2_scheme)], session: db_session):
    return books_service.export_books(token, session)

@router.get("/books/all",
    summary="Get books for all users",
    description="Retrieves books for all users as long as the user has an admin or librarian role")
def get_all_books(token: Annotated[str, Depends(oauth2_scheme)], session: db_session):
    return books_service.get_all_books(token, session)

@router.get("/books",
    summary="Get all books",
    description="Retrieves all books in the library or based on search filters author, title, year, available, pages, min pages, max pages, and sort by title, pages, year and order",
    responses={404: {"model": ErrorResponse}}
)
def get_books(token: Annotated[str, Depends(oauth2_scheme)], session: db_session, author: str | None = None, title: str | None = None,
    year: int | None = None, available: bool | None = None, pages: int | None = None,
    min_pages: int | None = None, max_pages: int | None = None, sort_by: str | None = None,
    order:str | None = None, limit: int | None = Query(default=None, gt=0),
    offset: int = Query(default=0, ge=0)):
    return books_service.get_books(
            token, session, author, title,
            year, available, pages,
            min_pages, max_pages, sort_by,
            order, limit, offset
    )

@router.get("/books/{book_id}",
    summary="Get book by id",
    description="Retrieves a book by it's id from the library",
    response_model=BookResponse,
    responses={404: {"model": ErrorResponse}})
def get_book_by_id(token: Annotated[str, Depends(oauth2_scheme)], book_id: int, session: db_session):
    return books_service.get_book_by_id(token, session, book_id)

@router.put("/books/{book_id}",
    summary="Update book by id",
    description="Updates the details of a book within library by it's id",
    response_model=BookUpdatedResponse,
    responses={404: {"model": ErrorResponse}}
    )
def update_book_by_id(token: Annotated[str, Depends(oauth2_scheme)], book_id: int, book_details: BookUpdateRequest,
    session: db_session):
    return books_service.update_book_by_id(token, session, book_id, book_details)

@router.delete("/books/{book_id}",
    summary="Remove a book",
    description="Removes a book by it's id from the library",
    response_model=BookDeletionResponse,
    responses={
        404: {"model": ErrorResponse}
    })
def delete_book_by_id(token: Annotated[str, Depends(oauth2_scheme)], book_id: int, session: db_session):
    return books_service.delete_book_by_id(token, session, book_id)
