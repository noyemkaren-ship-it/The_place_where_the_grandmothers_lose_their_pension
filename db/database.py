from typing import Generator

from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

from models.bet import Bet
from models.token import Token
from models.user import User

DB_URL = "sqlite:///casino.db"
engine = create_engine(DB_URL, echo=False)

def init_db():
    SQLModel.metadata.create_all(engine, tables=[User.__table__])
    # Потом создаем таблицы с внешними ключами
    SQLModel.metadata.create_all(engine, tables=[Token.__table__])
    SQLModel.metadata.create_all(engine, tables=[Bet.__table__])

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

init_db()