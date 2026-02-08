import json
import random
from typing import List

from fastapi import Depends, HTTPException, APIRouter
from passlib.context import CryptContext
from sqlmodel import Session, select

from api.depends import UserDepends
from db.database import get_session
from models.bet import Bet
from models.user import User
from shemas.bet import BetsResponse
from shemas.betout import BetOut
from shemas.coinflip import CoinflipRequest
from shemas.crash import CrashRequest
from shemas.dice import DiceRequest

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
    session.refresh(user)

    return {
        "result": "win" if win else "lose",
        "payout": payout,
        "balance": user.balance,
    }

@router.post("/games/dice")
def dice(
        payload: DiceRequest,
        session: Session = Depends(get_session),
        user: User = UserDepends
):
    if user.balance < payload.stake:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    roll = random.randint(1, 6)
    win = roll == payload.number
    payout = payload.stake * 6 if win else 0

    user.balance = user.balance - payload.stake + payout
    bet = Bet(
        user_id=user.id,
        game="dice",
        stake=payload.stake,
        selection_json=json.dumps({'number': payload.number}),

        outcome_json=json.dumps({'roll': roll, 'win': win}),
        payout=payout
    )

    session.add(bet)
    session.add(user)
    session.commit()
    session.refresh(user)

    return {
        "result": "win" if win else "lose",
        "payout": payout,
        "roll": roll,
        "balance": user.balance,
    }

@router.post("/games/crash")
def crash(
        payload: CrashRequest,
        session: Session = Depends(get_session),
        user: User = UserDepends
):
    if user.balance < payload.stake:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    final_multiplier = round(random.uniform(1.2, 5.0), 2)
    win = final_multiplier >= payload.cashout
    payout = int(round(payload.stake * payload.cashout)) if win else 0

    user.balance = user.balance - payload.stake + payout

    bet = Bet(
        user_id=user.id,
        game="crash",
        stake=payload.stake,
        selection_json=json.dumps({'number': payload.number}),
        outcome_json=json.dumps({"final_multiplier": final_multiplier, 'win': win}),
        payout=payout
    )
    session.add(bet)
    session.add(user)
    session.commit()
    session.refresh(user)

    return {
        "result": "win" if win else "lose",
        "payout": payout,
        "final_multiplier": final_multiplier,
        "balance": user.balance
    }

@router.get("/bets", response_model=BetsResponse)
def bets(
        session: Session = Depends(get_session),
        user: User = UserDepends
) -> BetsResponse:
    rows = (
        session.exec(
            select(Bet)
            .where(Bet.user_id == user.id)
            .order_by(Bet.created_at.desc())
            .limit(50)
        ).all())
    bets_out: List[BetOut] = []
    for row in rows:
        bets_out.append(BetOut(
            game=row.game,
            stake=row.stake,
            selection=json.loads(row.selection_json),
            outcome=json.loads(row.outcome_json),
            payout=row.payout,
            created_at=row.created_at,
        ))
    return BetsResponse(bets_out=bets_out)