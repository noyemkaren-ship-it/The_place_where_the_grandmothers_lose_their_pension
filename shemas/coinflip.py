from shemas.meresponse import MeResponse


class CoinflipRequest(MeResponse):
    stake: int
    choice: str
