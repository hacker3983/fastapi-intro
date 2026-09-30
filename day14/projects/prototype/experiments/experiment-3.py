from sqlalchemy import create_engine
from sqlalchemy import Integer
from sqlalchemy import select
from sqlalchemy.orm import (
    Session,
    DeclarativeBase,
    Mapped,
    mapped_column
)
from sqlalchemy.exc import IntegrityError

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
engine.echo = True
Base.metadata.create_all(engine)

vehicles = [
    Vehicle(
        id=3,
        name="Ford Mustang",
        description="V8 engine, loud exhaust",
        value=25000
    ),
    Vehicle(
        id=4,
        name="Tesla Model 3",
        description="Electric sedan with autopilot",
        value=32000
    ),
    Vehicle(
        id=5,
        name="Jeep Wrangler",
        description="Off-road ready with removable top",
        value=28000
    ),
    Vehicle(
        id=2,
        name="Mazda Miata",
        description="Slow car fast, incredible handling",
        value=18000
    )
]

try:
    with Session(engine) as session:
        for vehicle in vehicles:
            session.add(vehicle)
        session.commit()
except IntegrityError:
    print("Database successfully rolled back after integrity error!")

with Session(engine) as session:
    result = session.execute(
            select(Vehicle)
    ).all()
    print(result)
