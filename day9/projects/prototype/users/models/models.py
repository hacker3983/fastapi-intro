from pydantic import BaseModel
from .request import *

class UsersAPIStatus(BaseModel):
    name: str = "Users API"
    version: str = 1.0
    status: str = "Online"
