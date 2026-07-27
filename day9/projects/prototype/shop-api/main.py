from typing import Annotated
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from shop_db import *

app = FastAPI()
shop_db = ShopDB()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def user_exists_error(user_details):
    raise HTTPException(status_code=400, detail=f"The user {user_details.username} already exists!")

def product_not_found_error(product_id):
    raise HTTPException(status_code=404, detail=f"The product with id {product_id} was not found!")

def invalid_user_error():
    raise HTTPException(status_code=400, detail=f"The username or password is invalid... Please try again!")

def auth_error():
    raise HTTPException(status_code=400, detail=f"User authorization or access token invalid... Please try again!")

def product_exists_error(product_name):
    raise HTTPException(status_code=400, detail=f"The product {product_name} already exists!")

def password_mismatch_error():
    raise HTTPException(status_code=400, detail=f"The password doesn't match! Please try again...")

def new_product_model(token, product_details: ProductCreationRequest):
    response = shop_db.add_product(token, product_details)
    return response

@app.get("/")
def home():
    return ShopAPIStatus()

@app.post("/signup")
def signup(user_details: UserCreationRequest):
    if user_details.password != user_details.password_confirmation:
        password_mismatch_error()
    response = shop_db.add_user(user_details)
    if response is None:
        user_exists_error(user_details)
    return response

@app.post("/signin", response_model=UserSigninResponse)
def signin(token: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = shop_db.get_user_by_name(token.username)
    if not user:
        invalid_user_error()

    if not verify_password(token.password, user.password_hash):
        invalid_user_error()

    response = UserSigninResponse(
        access_token=user.access_token
    )
    return response

@app.post("/products", response_model=ProductCreationResponse)
def create_product(
    token: Annotated[str, Depends(oauth2_scheme)],
    product_details: ProductCreationRequest
):
    response = new_product_model(token, product_details)
    if response is None:
        auth_error()
    elif response == False:
        product_exists_error(product_details.name)
    return response

@app.get("/count", response_model=ProductCountResponse)
def get_product_count(token: Annotated[str, Depends(oauth2_scheme)]):
    response = shop_db.get_product_count(token)
    if response == False:
        auth_error()
    return response

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(
    token: Annotated[str, Depends(oauth2_scheme)],
    product_id: int
):
    product = shop_db.get_product(token, product_id)
    if product == False:
        auth_error()
    elif not product:
        product_not_found_error(product_id)
    return product

@app.get("/products", response_model=ProductsRetrievalResponse)
def get_products(token: Annotated[str, Depends(oauth2_scheme)]):
    products = shop_db.get_products(token)
    if products == False:
        auth_error()
    response = ProductsRetrievalResponse(
        data=products
    )
    return response

@app.put("/products/{product_id}", response_model=ProductUpdateResponse)
def update_product(
    token: Annotated[str, Depends(oauth2_scheme)],
    product_id: int,
    product_details: ProductUpdateRequest
):
    try:
        response = shop_db.update_product(token, product_id, product_details)
    except ProductExistsError:
        product_exists_error(product_details.name)
    if response == False:
        auth_error()
    elif not response:
        product_not_found_error(product_id)
    return response

@app.delete("/products/{product_id}", response_model=ProductDeletionResponse)
def remove_product(
    token: Annotated[str, Depends(oauth2_scheme)],
    product_id: int
):
    response = shop_db.remove_product(token, product_id)
    if response == False:
        auth_error()
    elif not response:
        product_not_found_error(product_id)
    return response
