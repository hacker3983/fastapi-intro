from pydantic import BaseModel

class LibraryAPIStatus(BaseModel):
    name: str = "Library API"
    version: float = 0.1
    status: str = "Online!"

class BookModel(BaseModel):
    title: str
    author: str
    year: int
    pages: int

class BookCreation(BookModel):
    id: int


class BookCreationUpdateResponse(BookModel):
    message: str
    data: BookCreation
