from pydantic import BaseModel
from .request import *
from .response import *
from .database import *

class ShopAPIStatus(BaseModel):
    name: str = "Shop API"
    version: float = 1.0
    status: str = "Online"
