from pydantic import BaseModel

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    year: int
    pages: int
    available: bool

class BookCreationResponse(BaseModel):
    message: str = "Book created"
    data: BookResponse

class BookUpdatedResponse(BaseModel):
    message: str = "Book updated"
    data: BookResponse

class BookDeletionResponse(BaseModel):
    message: str = "Book deleted"
    data: BookResponse
