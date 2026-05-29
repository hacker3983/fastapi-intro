from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class ItemAPIStatus(BaseModel):
    name: str = "Items API"
    version: float = 0.1
    status: str = "Online"

class Item(BaseModel):
    name: str
    description: str

class ItemCreation(BaseModel):
    id: int
    name: str
    description: str

class ItemCreationUpdateResponse(BaseModel):
    message: str
    item: ItemCreation

app = FastAPI()
items = []
item_id_counter = 0

def new_item_model(item: Item):
    global item_id_counter
    item_id_counter += 1
    item_model = {
            "id": item_id_counter,
            "name": item.name,
            "description": item.description
    }
    return item_model

def find_item_by_id(item_id):
    for i, item in enumerate(items):
        if item["id"] != item_id:
            continue
        return (i, item)
    return None

def product_notfound_error():
    return HTTPException(status_code=404, detail="The requested item or resource was not found!")

@app.get("/")
def home():
    return ItemAPIStatus()

@app.get("/items")
def get_items():
    return {"Items": items}

@app.get("/items/{item_id}")
def get_item_by_id(item_id: int):
    result = find_item_by_id(item_id)
    if not result:
        return product_notfound_error()
    item = result[1]
    return item

@app.post("/items")
def add_item(item: Item):
    new_item = new_item_model(item)
    creation_response = ItemCreationUpdateResponse(
            message="Item Created",
            item=new_item
    )
    items.append(new_item)
    return creation_response

@app.put("/items/{item_id}")
def update_item_details_by_id(item_id: int, item: Item):
    result = find_item_by_id(item_id)
    if not result:
        return product_notfound_error()
    item_ref = result[1]
    item_ref["name"] = item.name
    item_ref["description"] = item.description
    response = ItemCreationUpdateResponse(
        message="Item Updated",
        item=ItemCreation.model_validate(item_ref)
    )
    return response

@app.delete("/items/{item_id}")
def delete_item_by_id(item_id: int):
    result = find_item_by_id(item_id)
    if not result:
        return product_notfound_error()
    item_index = result[0]
    response = ItemCreationUpdateResponse(
            message="Deleted product",
            item=ItemCreation.model_validate(result[1])
    )
    items.pop(item_index)
    return response
