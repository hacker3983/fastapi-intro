from pydantic import BaseModel

class ShopAPIStatus(BaseModel):
    name: str = "SHop API"
    version: float = 0.2
    status: str = "Online!"

class Product(BaseModel):
    name: str
    price: int

class ProductCreation(BaseModel):
    id: int
    name: str
    price: int

class ProductCreationUpdateResponse(BaseModel):
    message: str
    data: ProductCreation

class ProductDeleteAllResponse(BaseModel):
    message: str
    data: list
