import json
import random

from fastapi import Depends, HTTPException, APIRouter
from passlib.context import CryptContext
from sqlmodel import Session

from api.depends import UserDepends
from db.database import get_session
from models.bet import Bet
from models.user import User
from shemas.coinflip import CoinflipRequest

pwd_context = CryptContext(schemes=['bcrypt'],
                           deprecated="auto")

router = APIRouter()


@router.post("/games/coinflip")
def coinflip(
        payload: CoinflipRequest,
        session: Session = Depends(get_session),
        user: User = UserDepends
):
    choice = payload.choice.strip().lower()
    if choice not in {"heads", "tails"}:
        raise HTTPException(status_code=400, detail="Иди гуляй отсюда")

    if user.balance < payload.stake:
        raise HTTPException(status_code=400, detail="Привет пупсик")

    server_choice = random.choice(["heads", "tails"])
    win = choice == server_choice
    payout = payload.stake * 2 if win else 0

    if win:
        user.balance = user.balance - payload.stake + payout
    else:
        user.balance = user.balance - payload.stake

    bet = Bet(
        user_id=user.id,
        game="coinflip",
        stake=payload.stake,
        selection_json=json.dumps({"choice": choice}),
        outcome_json=json.dumps({"server_choice": server_choice, "win": win}),
        payout=payout
    )

    session.add(bet)
    session.add(user)
    session.commit()
    session.refresh(bet)

    return {
        "result": "win" if win else "lose",
        "payout": payout,
        "balance": user.balance,
    }
