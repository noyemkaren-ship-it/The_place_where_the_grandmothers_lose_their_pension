from typing import Generator

from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel
DB_URL = "sqlite:///casino.db"
engine = create_engine(DB_URL, echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
