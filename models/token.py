from datetime import datetime

from sqlmodel import SQLModel, Field

class Token(SQLModel, table=True):
    token: str = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.now)
