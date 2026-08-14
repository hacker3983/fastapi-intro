from fastapi import FastAPI, HTTPException, status, Query
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from models import *
from library_db import *
from typing import Annotated

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")

my_library = LibraryDB()

def user_exists_error(username):
    raise HTTPException(
        status_code=400,
        detail=f"The user {username} already exists!"
    )

def invalid_user_error():
    raise HTTPException(
        status_code=401,
        detail="Invalid username or password! Please try again..."
    )

def invalid_token_error():
    raise HTTPException(
        status_code=401,
        detail="Invalid access token or authorization! Please try again..."
    )

def password_mismatch_error():
    raise HTTPException(
        status_code=401,
        detail="The password doesn't match! Please try again..."
    )

def new_book_model(token, book_details: BookCreationRequest):
    new_book = my_library.add_book(token, book_details)
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

@app.post("/signin",
    summary="Signs into a user",
    description="Logs into a user account and generates an access token can be used on endpoints. If user doesn't exist or password is invalid raises on error on the server",
    response_model=UserSigninResponse)
def signin(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = my_library.get_user_by_name(form_data.username)
    if not user:
        invalid_user_error()

    if not verify_password(form_data.password, user.password_hash):
        invalid_user_error()

    response = UserSigninResponse(
        username=form_data.username,
        access_token=generate_access_token(form_data.username)
    )
    return response

@app.post("/signup",
    summary="Signup for an account",
    description="Signups for a user account as long as the user doesn't exist. Stores the user information with hashed password with argon2 in the database.",
    status_code=status.HTTP_201_CREATED,
    response_model=UserCreationResponse)
def signup(creation_details: UserCreationRequest):
    if creation_details.password != creation_details.password_confirmation:
        password_mismatch_error()
    response = my_library.add_user(creation_details)
    if not response:
        user_exists_error(creation_details.username)
    return response

@app.post("/books",
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

@app.get("/books/count",
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

@app.get("/books/latest",
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

@app.get("/books/available",
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

@app.get("/books/unavailable",
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

@app.get("/books/stats", response_model=BookStatisticsResponse)
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

@app.post("/books/import", response_model=BookImportResponse,
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

@app.get("/books/export")
def export_books(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        result = my_library.get_books(token)
    except InvalidTokenError:
        invalid_token_error()
    return {"Books": result}

@app.get("/books",
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

@app.get("/books/{book_id}",
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

@app.put("/books/{book_id}",
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

@app.delete("/books/{book_id}",
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
