from pydantic import BaseModel

class MeResponse(BaseModel):
    email: str
    balance: int