from fastapi import FastAPI

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

def generate_product_query_error(product_id):
    return {"Query Error": f"No product found with id: '{product_id}'"}


@app.get("/")
def home():
    return {"Shop API": {"Status": "Online!"}}


@app.post("/products")
def create_product(name: str, price: int):
    product = new_product_model(name, price)
    products.append(product)
    return {"Successfully created product": product}

@app.get("/products")
def get_products():
    return {"Products": products}

@app.get("/products/{product_id}")
def get_product_by_id(product_id: int):
    result = find_product_by_id(product_id)
    if not result:
        return {"Query Error": f"No product found with id: '{product_id}'"}
    product = result[1]
    return product

@app.put("/products/{product_id}")
def update_product_price_by_id(product_id: int, price: int):
    result = find_product_by_id(product_id)
    if not result:
        return generate_product_query_error(product_id)
    product = result[1]
    product["price"] = price
    return {"Successfully updated product": product}

@app.delete("/products/{product_id}")
def delete_product_by_id(product_id: int):
    result = find_product_by_id(product_id)
    if not result:
        return generate_product_query_error(product_id)
    product_index = result[0]
    products.pop(product_index)
    return {"Successfully deleted product with id": product_id}
