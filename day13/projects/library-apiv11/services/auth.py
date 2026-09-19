from dependencies import my_library
from helpers import invalid_user_error, password_mismatch_error, user_exists_error
from library_db import verify_password, generate_access_token
from models import UserSigninResponse, UserCreationResponse, UserCreationRequest

def signin(session, form_data):
    user = my_library.get_user_by_name(session, form_data.username)
    if not user:
        invalid_user_error()

    if not verify_password(form_data.password, user.password_hash):
        invalid_user_error()

    response = UserSigninResponse(
        username=form_data.username,
        access_token=generate_access_token(form_data.username)
    )
    return response

def signup(session, creation_details):
    if creation_details.password != creation_details.password_confirmation:
        password_mismatch_error()
    response = my_library.add_user(session, creation_details)
    if not response:
        user_exists_error(creation_details.username)
    return response
