from models import BookImportResponse
from jwt.exceptions import InvalidTokenError
from dependencies import my_library, oauth2_scheme, db_session
from helpers import (
    invalid_restoration_error, invalid_token_error,
    book_creation_error, book_not_found_error,
    forbidden_access_error
)
from models import (
    BookRestorationResponse, BookCreationResponse, ErrorResponse,
    BookCreationRequest, BookCountResponse, BookLatestResponse,
    BookUpdateRequest,
    BookUpdatedResponse, BookDeletionResponse,
    BookAvailableResponse, BookUnavailableResponse, BookStatisticsResponse,
    BookImportRequest, BookImportResponse, BookResponse
)

def create_book(token, session, book_details):
    try:
        book = my_library.add_book(token, session, book_details)
    except InvalidTokenError:
        invalid_token_error()
    response = BookCreationResponse(
        data=book
    )
    return response

def import_books(token, session, book_details):
    book = None
    errors = []
    import_count = 0
    detail_list = book_details.books
    response = []
    for book_detail in detail_list:
        try:
            book = my_library.add_book(token, session, book_detail)
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

def restore_book(token, session, book_id):
    try:
        result = my_library.restore_book(token, session, book_id)
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

def get_books_count(token, session):
    try:
        result = my_library.get_book_count(token, session)
    except InvalidTokenError:
        invalid_token_error()
    return BookCountResponse(
            data=result
    )

def get_latest_book(token, session):
    try:
        result = my_library.get_latest_book(token, session)
    except InvalidTokenError:
        invalid_token_error()
    return BookLatestResponse(
        data=result
    )

def get_available_books(token, session):
    try:
        available_books = my_library.get_available_books(token, session)
    except InvalidTokenError:
        invalid_token_error()
    return BookAvailableResponse(
        data=available_books
    )

def get_unavailable_books(token, session):
    try:
        unavailable_books = my_library.get_unavailable_books(token, session)
    except InvalidTokenError:
        invalid_token_error()
    return BookUnavailableResponse(
        data=unavailable_books
    )

def get_books_statistics(token, session):
    try:
        book_stats = my_library.get_book_stats(token, session)
    except InvalidTokenError:
        invalid_token_error()
    return BookStatisticsResponse(
            total_books=book_stats["total_books"],
            available_books=book_stats["available_books"],
            unavailable_books=book_stats["unavailable_books"]
    )

def export_books(token, session):
    try:
        result = my_library.get_books(token, session)
    except InvalidTokenError:
        invalid_token_error()
    return result

def get_all_books(token, session):
    try:
        results = my_library.get_books(token, session, all_books=True)
    except InvalidTokenError:
        invalid_token_error()
    if results == False:
        forbidden_access_error()
    return {"Books": results}

def get_books(token, session, author, title, year,
    available, pages, min_pages, max_pages, sort_by, order, limit, offset):
    try:
        results = my_library.filter_books(token, session, author, title, year, available, pages, min_pages, max_pages,
        sort_by, order, limit, offset)
    except InvalidTokenError:
        invalid_token_error()
    if not results:
        book_not_found_error()
    results = {"Books": results}
    return results

def get_book_by_id(token, session, book_id):
    try:
        result = my_library.get_book_by_id(token, session, book_id)
    except InvalidTokenError:
        invalid_token_error()
    if not result:
        book_not_found_error(book_id)
    return result


def update_book_by_id(token, session, book_id, book_details):
    try:
        book = my_library.update_book(token, session, book_id, book_details)
    except InvalidTokenError:
        invalid_token_error()
    if not book:
        book_not_found_error(book_id)
    response = BookUpdatedResponse(
        data=book
    )
    return response


def delete_book_by_id(token, session, book_id):
    try:
        deleted_book = my_library.remove_book(token, session, book_id)
    except InvalidTokenError:
        invalid_token_error()
    if not deleted_book:
        book_not_found_error(book_id)
    response = BookDeletionResponse(
        data=deleted_book
    )
    return response
