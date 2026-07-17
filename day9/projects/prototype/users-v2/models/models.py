from pydantic import BaseModel
from .request import *
from .response import *

class UsersAPIStatus(BaseModel):
    name: str = "User API"
    version: float = 2.0
    status: str = "Online"
