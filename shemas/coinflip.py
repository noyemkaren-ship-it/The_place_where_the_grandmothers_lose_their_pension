from pydantic import Field
from sqlalchemy import Integer
from shemas.meresponse import MeResponse


class CoinflipRequest(MeResponse):
    stake: int = Field(gt=0)
    choice: str

