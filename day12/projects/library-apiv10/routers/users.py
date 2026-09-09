from fastapi import APIRouter, Depends
from dependencies import my_library, oauth2_scheme 
from helpers import invalid_token_error, forbidden_access_error, role_modification_error
from models import UserAccountsResponse
from jwt.exceptions import InvalidTokenError
from typing import Annotated

router = APIRouter()

@router.get("/users",
    summary="Gets all users",
    description="Returns a list of all users this is only accessible to admins or librarians",
    response_model=UserAccountsResponse)
def get_users(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        responses = my_library.get_users(token)
    except InvalidTokenError:
        invalid_token_error()
    if responses == False:
        forbidden_access_error()
    responses = UserAccountsResponse(
        data=responses
    )
    return responses

@router.get("/users/{user_id}",
    summary="Get details for a user by id",
    description="Returns the details of specific user only admins")
def get_user(token: Annotated[str, Depends(oauth2_scheme)], user_id: int):
    try:
        response = my_library.get_user(token, user_id)
    except InvalidTokenError:
        invalid_token_error()
    if response == False:
        forbidden_access_error()
    return response

@router.patch("/users/{user_id}/role",
    summary="Sets a users role",
    description="Modifies a users role only for admins")
def update_user_role(token: Annotated[str, Depends(oauth2_scheme)], user_id, role: str):
    try:
        response = my_library.modify_user_role(token, user_id, role)
    except InvalidTokenError:
        invalid_token_error()
    if response == False:
        forbidden_access_error()
    if response is None:
        role_modification_error()
    return response
