from typing import Annotated
from pydantic import BaseModel
from pydantic import Field

class UserCreationRequest(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    full_name: str = Field(min_lenth=1)
    password: str = Field(min_length=8)
    password_confirmation: str = Field(min_length=8)

class ProductCreationRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=300)
    value: int = Field(gt=0)

class ProductUpdateRequest(BaseModel):
    name: Annotated[str | None, Field(min_length=1, max_length=100)] = None
    description: Annotated[str | None, Field(min_length=1, max_length=300)] = None
    value: Annotated[int | None, Field(gt=0)] = None
