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

class BookCountResponse(BaseModel):
    message: str = "Book count"
    data: int

class BookLatestResponse(BaseModel):
    message: str = "Latest book"
    data: BookResponse | None = None

class BookAvailableResponse(BaseModel):
    message: str = "Available books"
    data: list[BookResponse]

class BookUnavailableResponse(BaseModel):
    message: str = "Unavailable books"
    data: list[BookResponse]

class BookStatisticsResponse(BaseModel):
    Total_books: int
    Available_books: int
    Unavailable_books: int
