from pydantic import BaseModel
from .requests import *
from .responses import *
from .database import *
from .errors import *

class LibraryAPIStatus(BaseModel):
    name: str = "Library API"
    version: float = 0.9
    status: str = "Online!"
