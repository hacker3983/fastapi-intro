from fastapi import Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from library_db import LibraryDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v10/signin")
my_library = LibraryDB()

def get_db():
    with Session(my_library.db) as session:
        yield session

db_session = Annotated[Session, Depends(get_db)]
