from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(default=None, unique=True)
    password_hash: str
    balance: int = 10000
