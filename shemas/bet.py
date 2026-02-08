from typing import List

from pydantic import BaseModel

from shemas.betout import BetOut


class BetsResponse(BaseModel):
    bets_out: List[BetOut]
