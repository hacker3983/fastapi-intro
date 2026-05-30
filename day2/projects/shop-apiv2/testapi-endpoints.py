import requests

endpoint_url = "http://localhost:8000"

def check_api_stats():
    print("[ * ] Checking API Status...")
    r = requests.get(endpoint_url)
    print(r.text)
    print("status_code:", r.status_code)
    print()

def create_product(name, price):
    print(f"[ * ] Creating product {name} with price {price}")
    r = requests.post(f"{endpoint_url}/products",
            json={
                "name": name,
                "price": price
            }
        )
    print(r.text)
    print()

def get_products():
    print("[ * ] List of products:")
    r = requests.get(f"{endpoint_url}/products")
    print(r.text)
    print()

def get_product_by_id(product_id):
    print(f"[ * ] Getting product with id {product_id}")
    r = requests.get(f"{endpoint_url}/products/{product_id}")
    print(r.text)
    print()

def update_product_price_by_id(product_id, product_name, product_price):
    print(f"[ * ] Updating product with id {product_id}")
    print(f"product_name --> {product_name}")
    print(f"product_price --> {product_price}")
    r = requests.put(f"{endpoint_url}/products/{product_id}",
        params={
            "price": product_price
        }
    )
    print(r.text)
    print()

def delete_product_by_id(product_id):
    print(f"[ * ] Removing product with id {product_id}")
    r = requests.delete(f"{endpoint_url}/products/{product_id}")
    print(r.text)
    print()

def delete_all_products():
    print("[ * ] Removing all products...")
    r = requests.delete(f"{endpoint_url}/deleteall")
    print(r.text)
    print()

def create_products(products: dict):
    for product_name in my_products:
        product_price = my_products[product_name]
        create_product(product_name, product_price)



my_products = {
        "Bread": 500,
        "Cheese": 150,
        "Chocolate": 200
}


check_api_stats()

create_products(my_products)
get_products()
get_product_by_id(0)
get_product_by_id(1)

update_product_price_by_id(1, "Bread", 1500)
get_product_by_id(1)
get_products()


update_product_price_by_id(2, "Cheese", 300)
get_product_by_id(2)
get_products()

delete_product_by_id(0)
delete_product_by_id(2)
delete_product_by_id(2)
delete_product_by_id(1)
delete_product_by_id(1)

get_products()

delete_product_by_id(3)
delete_product_by_id(3)
get_products()
get_product_by_id(3)

print("Recreating products to test delete all:")
create_products(my_products)

get_products()

delete_all_products()

get_products()
