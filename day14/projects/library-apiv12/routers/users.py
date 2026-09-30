from fastapi import APIRouter, Depends
from services import users as users_service
from dependencies import oauth2_scheme, db_session 
from models import UserAccountsResponse
from typing import Annotated

router = APIRouter()

@router.get("/users",
    summary="Gets all users",
    description="Returns a list of all users this is only accessible to admins or librarians",
    response_model=UserAccountsResponse)
def get_users(token: Annotated[str, Depends(oauth2_scheme)], session: db_session):
    responses = users_service.get_users(token, session)
    return responses

@router.get("/users/{user_id}",
    summary="Get details for a user by id",
    description="Returns the details of specific user only admins")
def get_user(token: Annotated[str, Depends(oauth2_scheme)], user_id: int, session: db_session):
    response = users_service.get_user(token, session, user_id)
    return response

@router.patch("/users/{user_id}/role",
    summary="Sets a users role",
    description="Modifies a users role only for admins")
def update_user_role(token: Annotated[str, Depends(oauth2_scheme)], user_id, role: str, session: db_session):
    response = users_service.update_user_role(token, session, user_id, role)
    return response
