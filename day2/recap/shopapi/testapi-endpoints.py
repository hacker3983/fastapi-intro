import requests

endpoint_url = "http://localhost:8000"

def get_status():
    print("[ * ] Checking API endpoint status")
    r = requests.get(endpoint_url)
    print(r.text)
    print("responded with status code:", r.status_code)

def create_product(name, price):
    print(f"[ * ] Creating product '{name}' with price '{price}'...") 
    r = requests.post(f"{endpoint_url}/products", params={"name":name, "price":price})
    print(r.text)

def create_products(product_dict):
    for name in product_dict:
        price = product_dict[name]
        create_product(name, price)

def get_products():
    r = requests.get(f"{endpoint_url}/products")
    print("List of products in the shop are:")
    print(r.text)

def get_product_by_id(product_id):
    r = requests.get(f"{endpoint_url}/products/{product_id}")
    print("Getting product with id:", product_id)
    print(r.text)

def update_product_price_by_id(product_id, price):
    r = requests.put(f"{endpoint_url}/products/{product_id}", params={"price": price})
    print(f"Updating product {product_id} with price {price}...")
    print(r.text)

def delete_product_by_id(product_id):
    r = requests.delete(f"{endpoint_url}/products/{product_id}")
    print(f"[ * ] Deleting product {product_id}...")
    print(r.text)

products = {"Bread":500, "Fish":1000, "Cheese":150,
            "Patty": 320}
get_status()
create_products(products)
print()

get_products()
print()

update_product_price_by_id(1, 1500)
print()

get_products()
print()

get_product_by_id(3)
print()

delete_product_by_id(1)
print()

delete_product_by_id(1)
print()

get_product_by_id(3)
print()

get_products()
print()

delete_product_by_id(2)
print()

get_product_by_id(2)
print()

get_products()
