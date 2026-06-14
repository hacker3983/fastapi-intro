from typing import Annotated
from pydantic import BaseModel, Field
from datetime import datetime

current_year = datetime.now().year

validation_messages = {
    "year": f"The year must be greater than zero and less than or equal to {current_year}",
    "pages": f"The pages must be greater than zero"
}

class BookCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=50)
    year: int = Field(
            gt=0,
            le=current_year,
            description=validation_messages["year"]
    )
    pages: int = Field(
        gt=0,
        description=validation_messages["pages"]
    )

class BookUpdateRequest(BaseModel):
    title: Annotated[str | None, Field(min_length=1, max_length=100)] = None
    author: Annotated[str | None, Field(min_length=1, max_length=50)] = None
    year: Annotated[int | None, Field(
            gt=0,
            le=current_year,
            description=validation_messages["year"]
    )] = None
    pages: Annotated[int | None, Field(
            gt=0,
            description=validation_messages["pages"]
    )] = None
    available: bool | None = None
