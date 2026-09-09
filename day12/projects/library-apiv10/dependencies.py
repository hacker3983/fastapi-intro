from fastapi.security import OAuth2PasswordBearer
from library_db import LibraryDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")
my_library = LibraryDB()
