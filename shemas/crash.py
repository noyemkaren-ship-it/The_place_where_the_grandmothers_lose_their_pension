from pydantic import BaseModel


class CrashRequest(BaseModel):
    stake: int
    cashout: float