import os
import json
import hashlib
from typing import Annotated
from fastapi import FastAPI
from fastapi import Depends
from fastapi import status
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from models.models import *

def users_data_to_dict_obj(users_data):
    new_obj = {}
    for username in users_data:
        new_obj[username] = dict(users_data[username])
    return new_obj

def json_to_users_response_model(json_data):
    new_users = {}
    for username in json_data:
        new_users[username] = UserResponse.model_validate(json_data[username])
    return new_users

def users_data_to_json_model(users_data, tokens_data):
    json_model = {
        "users": users_data,
        "tokens": tokens_data
    }
    return json_model

def restore_backup():
    with open("backups.json", "r") as backup_file:
        try:
            json_data = json.load(backup_file)
            with open("users.json", "w") as f:
                print("Successfully restored user's backup data...")
                json.dump(
                    users_data_to_json_model(
                        json_data['users'],
                        json_data['tokens']
                    ),
                    f,
                    indent=2
                )
        except json.decoder.JSONDecodeError:
            print("Failed to restore user's backup data...")

def load_data():
    global users_info, tokens_info
    create_backup = False
    if not os.path.isfile("users.json") and os.path.isfile("backups.json"):
        restore_backup()
    elif not os.path.isfile("users.json"):
        return
    elif os.path.isfile("users.json") and not os.path.isfile("backups.json"):
        create_backup = True
    with open("users.json") as f:
        try:
            json_data = json.load(f)
            users_info = json_to_users_response_model(json_data['users'])
            tokens_info = json_data['tokens']
            if create_backup:
                print("Creating backup for users data...")
                save_data()
        except json.decoder.JSONDecodeError:
            print("Failed to load user's data...")
            return
    print("Successfully loaded user's data...")

def save_data():
    with open("users.json", "w") as f:
        json.dump(
            users_data_to_json_model(
                users_data_to_dict_obj(users_info),
                tokens_info
            ),
            f,
            indent=2
        )
        with open("backups.json", "w") as backup_file:
            json.dump(
                users_data_to_json_model(
                    users_data_to_dict_obj(users_info),
                    tokens_info
                ),
                backup_file,
                indent=2
            )
    print("Successfully saved user's data...")

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
users_info = {}
tokens_info = {}
load_data()

def generate_permanent_access_token(username, password):
    access_token = hashlib.sha256(f"{username}{password}".encode()).hexdigest()
    return access_token

def new_user_model(user_details: UserSignupRequest):
    if user_details.username in users_info:
        return None
    new_user = UserResponse(
        username=user_details.username,
        password_hash=hashlib.sha256(user_details.password.encode()).hexdigest(),
        age=user_details.age,
        occupation=user_details.occupation,
        birth_year=user_details.birth_year,
        birth_month=user_details.birth_month,
        birth_day=user_details.birth_day
    )
    return new_user

def user_exists_error(user_details: UserSignupRequest):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"The user {user_details.username} already exists!"
    )

def password_mismatch_error():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"The password doesn't match! Please try again..."
    )

def create_user_account(user_details: UserSignupRequest):
    new_user = new_user_model(user_details)
    if not new_user:
        user_exists_error(user_details)
    if user_details.password != user_details.password_confirmation:
        password_mismatch_error()
    users_info.update({user_details.username: new_user})
    access_token = generate_permanent_access_token(
        user_details.username,
        user_details.password
    )
    tokens_info.update({user_details.username: access_token})
    return new_user

def invalid_account_error():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid username or password! Please try again..."
    )

def retrieval_error():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to retrieve data! Invalid access token or authorization..."
    )

def find_user_by_token(token):
    usernames = list(tokens_info)
    result = None
    try:
        username = usernames[
            list(tokens_info.values()).
            index(token)
        ]
        result = (username, users_info[username])
    except ValueError:
        pass
    return result

@app.get("/")
def home():
    return UsersAPIStatus()

@app.post("/token")
def login(token: Annotated[OAuth2PasswordRequestForm, Depends()]):
    access_token = tokens_info.get(token.username)
    if not access_token:
        invalid_account_error()
    password_hash = hashlib.sha256(token.password.encode()).hexdigest()
    user_info = users_info.get(token.username)
    if user_info is None or password_hash != user_info.password_hash:
        invalid_account_error()
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/signup", response_model=UserSignupResponse)
def signup(user_details: UserSignupRequest):
    new_user = create_user_account(user_details)
    response = UserSignupResponse(
            data=UserResponse.model_validate(new_user)
    )
    save_data()
    return response

@app.get("/details", response_model=UserRetrievalResponse)
def retrieve_details(token: Annotated[str, Depends(oauth2_scheme)]):
    result = find_user_by_token(token)
    if not result:
        retrieval_error()
    user_info = result[1]
    response = UserRetrievalResponse(data=user_info)
    return response

@app.put("/update", response_model=UserUpdateResponse)
def update_details(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_details: UserUpdateRequest
):
    result = find_user_by_token(token)
    if not result:
        retrieval_error()
    username, user_info = result
    updated = False
    if user_details.username:
        if user_details.username in users_info:
            user_exists_error(user_details)
        new_username = user_details.username
        user_info.username = new_username
        users_info[new_username] = users_info.pop(username)
        tokens_info[new_username] = tokens_info.pop(username)
        username = new_username
        updated = True

    if user_details.password:
        user_info.password_hash = hashlib.sha256(user_details.password.encode()).hexdigest()
        tokens_info[username] = generate_permanent_access_token(username, user_details.password)
        updated = True

    if user_details.age:
        user_info.age = user_details.age
        updated = True

    if user_details.occupation:
        user_info.occupation = user_details.occupation
        updated = True

    if user_details.birth_year:
        user_info.birth_year = user_details.birth_year
        updated = True

    if user_details.birth_month:
        user_info.birth_month = user_details.birth_month
        updated = True

    if user_details.birth_day:
        user_info.birth_day = user_details.birth_day
        updated = True
    
    response = UserUpdateResponse(
        data=user_info
    )
    if not updated:
        response.status = False
    save_data()
    return response

@app.delete("/delete")
def delete_user_account(token: Annotated[str, Depends(oauth2_scheme)]):
    result = find_user_by_token(token)
    if not result:
        retrieval_error()
    username, user_info = result
    response = UserDeletionResponse(
        data=user_info
    )
    try:
        users_info.pop(username)
        tokens_info.pop(username)
    except:
        retrieval_error()
    save_data()
    return response
