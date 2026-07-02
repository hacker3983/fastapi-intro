from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Books(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
    year: Mapped[int]
    pages: Mapped[int]
    available: Mapped[bool]

    def __repr__(self):
        return f"Book(id={self.id!r}, title={self.title!r}, author={self.author!r}, year={self.year!r}, pages={self.pages!r}, available={self.available!r})"
