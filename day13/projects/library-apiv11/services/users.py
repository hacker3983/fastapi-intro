from dependencies import my_library
from helpers import invalid_token_error, forbidden_access_error, role_modification_error
from models import UserAccountsResponse
from jwt.exceptions import InvalidTokenError

def get_users(token, session):
    try:
        responses = my_library.get_users(token, session)
    except InvalidTokenError:
        invalid_token_error()
    if responses == False:
        forbidden_access_error()
    responses = UserAccountsResponse(
        data=responses
    )
    return responses

def get_user(token, session, user_id):
    try:
        response = my_library.get_user(token, session, user_id)
    except InvalidTokenError:
        invalid_token_error()
    if response == False:
        forbidden_access_error()
    return response

def update_user_role(token, session, user_id, role):
    try:
        response = my_library.modify_user_role(token, session, user_id, role)
    except InvalidTokenError:
        invalid_token_error()
    if response == False:
        forbidden_access_error()
    if response is None:
        role_modification_error()
    return response
