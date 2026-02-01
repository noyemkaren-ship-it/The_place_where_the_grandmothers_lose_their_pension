from pydantic import BaseModel


class DiceRequest(BaseModel):
    stake: int
    number: int
