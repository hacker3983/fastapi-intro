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

try:
    with Session(engine) as session:
        conflict_vehicle = Vehicle(
            id=1,
            name="Subaru Impreza",
            description="Trying to steal ID 1",
            value=15000
    
        )
        session.add(conflict_vehicle)
        session.commit()
except IntegrityError:
    print("Database successfully rolled back after integrity error!")

with Session(engine) as session:
    result = session.execute(
            select(Vehicle)
    ).all()
    print(result)
