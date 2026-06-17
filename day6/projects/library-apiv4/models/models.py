from pydantic import BaseModel, Field
from .requests import *
from .responses import *
from .errors import *

class LibraryAPIStatus(BaseModel):
    name: str = "Library API"
    version: float = 0.4
    status: str = "Online!"
