from pydantic import BaseModel

class UserSigninResponse(BaseModel):
    signed_in: bool = True
    access_token: str
    token_type: str = "bearer"

class UserCreationDetails(BaseModel):
    username: str
    full_name: str

class UserCreationResponse(BaseModel):
    status: bool = True
    message: str = "Successfully Created User"
    data: UserCreationDetails

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    value: int

class ProductCountResponse(BaseModel):
    status: bool = True
    message: str = "Successfully Retrieved Product Count"
    product_count: int

class ProductCreationResponse(BaseModel):
    status: bool = True
    message: str = "Successfully Created Product"
    data: ProductResponse

class ProductsRetrievalResponse(BaseModel):
    status: bool = True
    message: str = "Successfully Retrieved Products"
    data: list[ProductResponse] | None = None

class ProductUpdateResponse(BaseModel):
    status: bool = True
    message: str = "Successfully Updated Product"
    data: ProductResponse

class ProductDeletionResponse(BaseModel):
    status: bool = True
    message: str = "Successfully Deleted Product"
    data: ProductResponse
