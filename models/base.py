from typing import Optional

from sqlalchemy.orm.decl_api import declared_attr
from sqlmodel import SQLModel, Field


class BaseCustomModel(SQLModel):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()