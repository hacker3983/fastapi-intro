from pydantic import BaseModel

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    value: int

class ProductCreationResponse(BaseModel):
    status: str = "Success"
    message: str = "Successfully Created Product"
    data: ProductResponse

class ProductsRetrievalResponse(BaseModel):
    status: str = "Success"
    message: str = "Successfully Retrieved Products"
    data: list[ProductResponse]

class ProductUpdateResponse(BaseModel):
    status: str = "Success"
    message: str = "Successfully Updated Product"
    data: ProductResponse

class ProductDeletionResponse(BaseModel):
    status: str = "Sucesss"
    message: str = "Successfully Deleted Product"
    data: ProductResponse
