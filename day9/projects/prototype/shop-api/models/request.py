from typing import Annotated
from pydantic import BaseModel
from pydantic import Field

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserCreationRequest(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=8)

class ProductCreationRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=300)
    value: int = Field(gt=0)

class ProductUpdateRequest(BaseModel):
    name: Annotated[str | None, Field(min_length=1, max_length=100)] = None
    description: Annotated[str | None, Field(min_length=1, max_length=300)] = None
    value: Annotated[int | None, Field(gt=0)] = None
