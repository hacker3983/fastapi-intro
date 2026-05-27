from fastapi import FastAPI

products = []
product_id_counter = 0

app = FastAPI()

def new_product_model(name, price):
    global product_id_counter
    product_model = {
        "id": product_id_counter,
        "name": name,
        "price": price
    }
    product_id_counter += 1
    return product_model

def find_productby_id(product_id):
    for i, product in enumerate(products):
        if product["id"] != product_id:
            continue
        return (i, product,)
    return None

@app.get("/")
def home():
    return {"Shop API Status": "Ok!"}

@app.post("/products")
def create_product(name: str, price: int):
    new_product = new_product_model(name, price)
    products.append(new_product)
    return {"Successfully created product": new_product}

@app.get("/products")
def get_products():
    return {"Products": products}

@app.get("/products/{product_id}")
def get_product_byid(product_id: int):
    result = find_productby_id(product_id)
    if not result:
        return {"Product ID Error": f"Invalid product id '{product_id}'!"}
    product = result[1]
    return product

@app.put("/products")
def update_productprice_byid(product_id: int, price: int):
    result = find_productby_id(product_id)
    if not result:
        return {"Product ID Error": f"Invalid product id '{product_id}'!"}
    product = result[1]
    product["price"] = price
    return {"Sucessfully updated product price": product}

@app.delete("/products")
def delete_productby_id(product_id: int):
    result = find_productby_id(product_id)
    if not result:
        return {"Product ID Error": f"invalid product id '{product_id}'!"}
    product_index = result[0]
    products.pop(product_index)
    return {"Successfully deleted product": product_id}
