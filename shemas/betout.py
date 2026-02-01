from datetime import datetime
from typing import Any, Dict, List

from pydantic import BaseModel

class BetOut(BaseModel):
    game: str
    stake: int
    selection: Dict[str, Any]
    outcome: Dict[str, Any]
    payout: int
    created_at: datetime

class BetResponse(BaseModel):
    bets: List[BetOut]
    notice: str
