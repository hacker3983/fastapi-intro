from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from dependencies import db_session
from services import auth as auth_service
from models import UserSigninResponse, UserCreationResponse, UserCreationRequest
from typing import Annotated

router = APIRouter()

@router.post("/signin",
    summary="Signs into a user",
    description="Logs into a user account and generates an access token can be used on endpoints. If user doesn't exist or password is invalid raises on error on the server",
    response_model=UserSigninResponse)
def signin(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: db_session):
    response = auth_service.signin(session, form_data)
    return response

@router.post("/signup",
    summary="Signup for an account",
    description="Signups for a user account as long as the user doesn't exist. Stores the user information with hashed password with argon2 in the database.",
    status_code=status.HTTP_201_CREATED,
    response_model=UserCreationResponse)
def signup(creation_details: UserCreationRequest, session: db_session):
    response = auth_service.signup(session, creation_details)
    return response
