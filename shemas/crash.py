from pydantic import BaseModel, Field


class CrashRequest(BaseModel):
    stake: int
    cashout: float = Field(ge=1.2, le=5.0)