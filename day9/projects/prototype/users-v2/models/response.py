from pydantic import BaseModel

class UserResponse(BaseModel):
    username: str
    password_hash: str
    age: int
    occupation: str
    birth_year: int
    birth_month: int
    birth_day: int

class UserSignupResponse(BaseModel):
    message: str = "Successfully created user account"
    status: bool = True
    data: UserResponse

class UserRetrievalResponse(BaseModel):
    message: str = "Successfully retrieved user details"
    status: bool = True
    data: UserResponse

class UserUpdateResponse(BaseModel):
    message: str = "Successfully updated user details"
    status: bool = True
    data: UserResponse

class UserDeletionResponse(BaseModel):
    message: str = "Successfully deleted user"
    status: bool = True
    data: UserResponse
