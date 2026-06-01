from pydantic import BaseModel, Field

class LibraryAPIStatus(BaseModel):
    name: str = "Library API"
    version: float = 0.1
    status: str = "Online!"

class BookModel(BaseModel):
    title: str = Field(min_length=1) 
    author: str = Field(min_length=1)
    year: int = Field(gt=0, description="The year must be greater than zero")
    pages: int = Field(gt=0, description="The pages must be greater than zero")
    available: bool = False

class BookCreation(BookModel):
    id: int


class BookCreationUpdateResponse(BaseModel):
    message: str
    data: BookCreation
