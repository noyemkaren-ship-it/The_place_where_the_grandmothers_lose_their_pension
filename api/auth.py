import uuid

from fastapi import Depends, HTTPException, APIRouter
from sqlmodel import Session, select

from api.depends import UserDepends
from db.database import get_session
from models.token import Token
from models.user import User
from shemas.auth import AuthRequest
from shemas.meresponse import MeResponse
from shemas.tokenresponse import TokenResponse
from utils import verify_password, hash_password

router = APIRouter()


@router.post("/auth/login", response_model=TokenResponse)
async def login(payload: AuthRequest, session: Session = Depends(get_session)) -> TokenResponse:
    user = session.exec(select(User).where(User.email == payload.email)).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    token = uuid.uuid4().hex

    session.add(
        Token(token=token, user_id=user.id)
    )

    session.commit()

    return TokenResponse(token=token)


@router.post("/auth/register", response_model=TokenResponse)
async def register(payload: AuthRequest, session: Session = Depends(get_session)) -> TokenResponse:
    existing = session.exec(select(User).where(User.email == payload.email)).first()
    if existing:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        balance=1000
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    token = uuid.uuid4().hex
    session.add(
        Token(token=token, user_id=user.id)
    )
    session.commit()

    return TokenResponse(token=token)


@router.get("/me", response_model=MeResponse)
async def me(user: User = UserDepends) -> MeResponse:
    return MeResponse(email=user.email, balance=user.balance)
