from typing import Annotated
from pydantic import BaseModel
from pydantic import Field

class UserSignupRequest(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=8)
    password_confirmation: str = Field(min_length=8)
    age: int = Field(gt=0)
    occupation: str = Field(min_length=1, max_length=50)
    birth_year: int = Field(gt=0)
    birth_month: int = Field(gt=0, le=12)
    birth_day: int = Field(gt=0, le=31)

class UserUpdateRequest(BaseModel):
    username: Annotated[
        str | None,
        Field(min_length=1, max_length=100)
    ] = None
    password: Annotated[
        str | None,
        Field(min_length=8)
    ] = None
    age: Annotated[
        int | None,
        Field(gt=0)
    ] = None
    occupation: Annotated[
        str | None,
        Field(min_length=1, max_length=50)
    ] = None
    birth_year: Annotated[
            int | None,
            Field(gt=0)
    ] = None
    birth_month: Annotated[int | None, Field(gt=0, le=12)] = None
    birth_day: Annotated[int | None, Field(gt=0, le=31)] = None
