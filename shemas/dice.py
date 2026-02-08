from pydantic import BaseModel, Field


class DiceRequest(BaseModel):
    stake: int
    number: int = Field(le=6, ge=1)
