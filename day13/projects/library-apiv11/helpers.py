from fastapi import HTTPException

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

def forbidden_access_error():
    raise HTTPException(
        status_code=403,
        detail="Sorry you do not have permission to perform the following operation..."
    )

def role_modification_error():
    raise HTTPException(
        status_code=404,
        detail="Failed to modify role either the role is invalid or the user id is invalid! Please try again..."
    )

def invalid_restoration_error():
    raise HTTPException(
        status_code=404,
        detail="There is no such resource or book to be restored! Please try again..."
    )

def password_mismatch_error():
    raise HTTPException(
        status_code=401,
        detail="The password doesn't match! Please try again..."
    )

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
