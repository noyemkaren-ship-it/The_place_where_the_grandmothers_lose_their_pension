from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class Bet(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="User.id", index=True)
    game: str
    stake: int
    selection_json: str
    outcome_json: str
    payout: int
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)