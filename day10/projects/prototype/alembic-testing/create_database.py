from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import Session

engine = create_engine("sqlite+pysqlite:///foods.db")
engine.echo = True
class Base(DeclarativeBase):
    pass

class Food(Base):
    __tablename__ = "food"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    value: Mapped[int]

    def __repr__(self):
        return f"Food(id={self.id!r}, name={self.name!r}, value={self.value!r})"


Base.metadata.create_all(engine)

foods = [
    Food(name="Apple", value=40),
    Food(name="Banana", value=50),
    Food(name="Mango", value=60),
    Food(name="Pineapple", value=100)
]

with Session(engine) as session:
    for food in foods:
        session.add(food)
    session.commit()
session.close()
