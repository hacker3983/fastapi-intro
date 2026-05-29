import requests

endpoint_url = "http://localhost:8000"

def check_api_stats():
    print("[ * ] Checking API Status...")
    r = requests.get(endpoint_url)
    print(r.text)
    print("status_code:", r.status_code)
    print()

def create_item(name, description):
    print(f"[ * ] Creating item {name} with description {description}")
    r = requests.post(f"{endpoint_url}/items",
            json={
                "name": name,
                "description": description
            }
        )
    print(r.text)
    print()

def get_items():
    print("[ * ] List of items:")
    r = requests.get(f"{endpoint_url}/items")
    print(r.text)
    print()

def get_item_by_id(item_id):
    print(f"[ * ] Getting item with id {item_id}")
    r = requests.get(f"{endpoint_url}/items/{item_id}")
    print(r.text)
    print()

def update_item_by_id(item_id, item_name, item_description):
    print(f"[ * ] Updating item with id {item_id}")
    print(f"item_name --> {item_name}")
    print(f"item_description --> {item_description}")
    r = requests.put(f"{endpoint_url}/items/{item_id}",
        json={
            "name": item_name,
            "description": item_description
        }
    )
    print(r.text)
    print()

def delete_item_by_id(item_id):
    print(f"[ * ] Removing item with id {item_id}")
    r = requests.delete(f"{endpoint_url}/items/{item_id}")
    print(r.text)
    print()


my_items = {
        "Bread": "A baked product with flour, wheat or other ingredients can be used to make sandwiches.",
        "Cheese": "A product made up with milk normally yellow and can be used to add flavor to things you are making can be used inside of sandwiches.",
        "Chocolate": "A naturally growing plant that is dark and can be used to make delicious things."
}


check_api_stats()

for item_name in my_items:
    item_description = my_items[item_name]
    create_item(item_name, item_description)

get_items()
get_item_by_id(0)
get_item_by_id(1)

update_item_by_id(1, "Bread", "Just some bread bro.")
get_item_by_id(1)
get_items()


update_item_by_id(2, "Cheese", "Just some cheese bro.")
get_item_by_id(2)
get_items()

delete_item_by_id(0)
delete_item_by_id(2)
delete_item_by_id(2)
delete_item_by_id(1)
delete_item_by_id(1)

get_items()

delete_item_by_id(3)
delete_item_by_id(3)
get_items()
get_item_by_id(3)
