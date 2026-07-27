from typing import List
import sqlalchemy
from sqlalchemy import String, Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
import hashlib

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"

    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    username:Mapped[str] = mapped_column(String(50))
    full_name:Mapped[str]
    password_hash:Mapped[str]
    access_token:Mapped[str]
    products:Mapped[List["Product"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r}, full_name={self.full_name!r}, password_hash={self.password_hash!r}, access_token={self.access_token!r}, products={self.products!r})"

class Product(Base):
    __tablename__ = "product"

    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey("user_account.id"))
    name:Mapped[str] = mapped_column(String(100))
    description:Mapped[str] = mapped_column(String(300))
    value:Mapped[int]

    user:Mapped[User] = relationship(back_populates="products")

    def __repr__(self):
        return f"Product(id={self.id!r}, user_id={self.user_id!r}, name={self.name!r}, description={self.description!r}, value={self.value!r})"
