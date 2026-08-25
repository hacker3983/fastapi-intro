from datetime import datetime
from pydantic import BaseModel

class UserCreationResponse(BaseModel):
    status: bool = True
    message: str = "Successfully Created User Account!"
    username: str
    fullname: str

class UserSigninResponse(BaseModel):
    status: bool = True
    message: str = "Successfully Signed into User Account!"
    username: str
    access_token: str
    token_type: str = "Bearer"

class UserResponse(BaseModel):
    id: int
    username: str
    role: str

class UserAccountsResponse(BaseModel):
    message: str = "Successfully retrieve user accounts!"
    data: list[UserResponse]

class BookResponse(BaseModel):
    id: int
    user_id: int
    title: str
    author: str
    year: int
    pages: int
    available: bool

    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

class BookCreationResponse(BaseModel):
    message: str = "Book created"
    data: BookResponse

class BookUpdatedResponse(BaseModel):
    message: str = "Book updated"
    data: BookResponse

class BookDeletionResponse(BaseModel):
    message: str = "Book deleted"
    data: BookResponse

class BookImportResponse(BaseModel):
    message: str = "Books imported"
    data: list[BookResponse]

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
    total_books: int
    available_books: int
    unavailable_books: int

class BookRestorationResponse(BaseModel):
    message: str = "Book restored"
    data: BookResponse
