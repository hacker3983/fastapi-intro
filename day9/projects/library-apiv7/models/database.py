from typing import List
from sqlalchemy import Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str]
    password_hash: Mapped[str]

    books: Mapped[List["Books"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r}, password_hash={self.password_hash!r}, books={self.books!r})"


class Books(Base):
    __tablename__ = "books"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_account.id"))

    title: Mapped[str]
    author: Mapped[str]
    year: Mapped[int]
    pages: Mapped[int]
    available: Mapped[bool]

    user: Mapped[User] = relationship(back_populates="books")

    def __repr__(self):
        return f"Book(id={self.id!r}, user_id={self.user_id!r}, title={self.title!r}, author={self.author!r}, year={self.year!r}, pages={self.pages!r}, available={self.available!r})"
