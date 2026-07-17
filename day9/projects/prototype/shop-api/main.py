from typing import Annotated
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from shop_db import *

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
shop_db = ShopDB()

def new_product_model(product_details: ProductCreationRequest):
    response = shop_db.add_product(product_details)
    return response

def product_not_found_error(product_id):
    raise HTTPException(status_code=404, detail=f"The product with id {product_id} was not found!")

@app.get("/")
def home():
    return ShopAPIStatus()

@app.get("/seetoken")
def get_token(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

@app.post("/products", response_model=ProductCreationResponse)
def create_product(
    token: Annotated[str, Depends(oauth2_scheme)],
    product_details: ProductCreationRequest
):
    response = new_product_model(product_details)
    return response

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(
    token: Annotated[str, Depends(oauth2_scheme)],
    product_id: int
):
    product = shop_db.get_product(product_id)
    if not product:
        product_not_found_error(product_id)
    return product

@app.get("/products", response_model=ProductsRetrievalResponse)
def get_products(token: Annotated[str, Depends(oauth2_scheme)]):
    products = shop_db.get_products()
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
    response = shop_db.update_product(product_id, product_details)
    if not response:
        product_not_found_error(product_id)
    return response

@app.delete("/products/{product_id}", response_model=ProductDeletionResponse)
def remove_product(
    token: Annotated[str, Depends(oauth2_scheme)],
    product_id: int
):
    response = shop_db.remove_product(product_id)
    if not response:
        product_not_found_error(product_id)
    return response
