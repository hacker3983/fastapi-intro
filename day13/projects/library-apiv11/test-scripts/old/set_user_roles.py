from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models.database import *

roles = [
    "admin",
    "librarian",
    "user",
    "user"
]

engine = create_engine("sqlite+pysqlite:///library.db")
with Session(engine) as session:
    for i, role in enumerate(roles):
        user = session.get(User, i+1)
        user.role = role
    session.commit()
