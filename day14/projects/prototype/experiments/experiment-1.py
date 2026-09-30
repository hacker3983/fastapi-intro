from sqlalchemy import create_engine
from sqlalchemy import Integer
from sqlalchemy import select
from sqlalchemy.orm import (
    Session,
    DeclarativeBase,
    Mapped,
    mapped_column
)

class Base(DeclarativeBase):
    pass

class Vehicle(Base):
    __tablename__ = "vehicle"

    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    name:Mapped[str]
    description:Mapped[str]
    value:Mapped[int]

    def __repr__(self):
        return f"Vehicle(id={self.id}, name={self.name}, description={self.description}, value={self.value})"

engine = create_engine("sqlite+pysqlite:///test.db")
Base.metadata.create_all(engine)

vehicles = [
    Vehicle(
        name="Honda Civic",
        description="Car with 1000 miles on it",
        value=9000
    ),
    Vehicle(
        name="Toyota Corolla",
        description="Car with 2000 miles on it",
        value=5000
    )
]

with Session(engine) as session:
    for vehicle in vehicles:
        session.add(vehicle)
    session.commit()

with Session(engine) as session:
    result = session.execute(
            select(Vehicle)
    ).all()
    print(result)
