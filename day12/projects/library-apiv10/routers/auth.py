from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from dependencies import my_library
from helpers import invalid_user_error, password_mismatch_error, user_exists_error
from library_db import verify_password, generate_access_token
from models import UserSigninResponse, UserCreationResponse, UserCreationRequest
from typing import Annotated

router = APIRouter()

@router.post("/signin",
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

@router.post("/signup",
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
