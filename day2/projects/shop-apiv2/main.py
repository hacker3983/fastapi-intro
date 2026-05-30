from fastapi import FastAPI, HTTPException
from models import *

app = FastAPI()

products = []
product_id_counter = 0
query_error = ""

def new_product_model(name, price):
    global product_id_counter
    product_id_counter += 1
    new_product = {
            "id": product_id_counter,
            "name": name,
            "price": price
    }
    return new_product

def find_product_by_id(product_id):
    for i, product in enumerate(products):
        if product["id"] != product_id:
            continue
        return (i, product)
    return None

def product_notfound_error():
    raise HTTPException(
        status_code=404,
        detail="The requested product or resource was not found!"
    )

@app.get("/")
def home():
    return ShopAPIStatus() 

@app.post("/products")
def create_product(product_details: Product):
    product = new_product_model(product_details.name, product_details.price)
    products.append(product)
    response = ProductCreationUpdateResponse(
        message="Product created",
        data=ProductCreation.model_validate(product)
    )
    return response

@app.get("/products")
def get_products():
    return {"Products": products}

@app.get("/products/{product_id}")
def get_product_by_id(product_id: int):
    result = find_product_by_id(product_id)
    if not result:
        product_notfound_error()
    product = result[1]
    return product

@app.put("/products/{product_id}")
def update_product_price_by_id(product_id: int, price: int):
    result = find_product_by_id(product_id)
    if not result:
        product_notfound_error()
    product = result[1]
    product["price"] = price
    response = ProductCreationUpdateResponse(
        message="Product updated",
        data=ProductCreation.model_validate(product)
    )
    return response


# I noticed fast api uvicorn server is interpreting /products/all
# in a delete request as an id so I had to change the endpoint to
# /deleteall/
@app.delete("/deleteall")
def delete_all_products():
    global product_id_counter
    products.clear()
    response = ProductDeleteAllResponse(
        message="Products deleted",
        data=products
    )
    product_id_counter = 0
    return response

@app.delete("/products/{product_id}")
def delete_product_by_id(product_id: int):
    result = find_product_by_id(product_id)
    if not result:
        product_notfound_error()
    product = result[1]
    product_index = result[0]
    response = ProductCreationUpdateResponse(
        message="Product deleted",
        data=ProductCreation.model_validate(product)
    )
    products.pop(product_index)
    return response
