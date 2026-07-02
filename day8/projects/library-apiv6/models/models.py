from pydantic import BaseModel, Field
from .requests import *
from .responses import *
from .errors import *
from .database import *

class LibraryAPIStatus(BaseModel):
    name: str = "Library API"
    version: float = 0.6
    status: str = "Online!"
