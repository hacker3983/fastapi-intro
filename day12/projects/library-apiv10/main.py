from fastapi import FastAPI, HTTPException, status, Query
from models import *
from routers import auth_router, users_router, books_router

app = FastAPI()
app.include_router(auth_router, prefix="/api/v10", tags=["Authentication"])
app.include_router(users_router, prefix="/api/v10", tags=["Users"])
app.include_router(books_router, prefix="/api/v10", tags=["Books"])

@app.get("/", summary="Get API info",
    description="Retrieves information about the api such as status, version info, etc",
    response_model=LibraryAPIStatus)
def home():
    return LibraryAPIStatus()
