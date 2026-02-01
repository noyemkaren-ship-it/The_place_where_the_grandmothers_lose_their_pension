from fastapi import Depends, Header
from passlib.context import CryptContext
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from starlette.exceptions import HTTPException

from db.database import get_session
from models.token import Token
from models.user import User

pwd_context = CryptContext(schemes=['bcrypt'],
                           deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def get_current_user(
        authorization: str | None = Header(default=None),
        session: Session = Depends(get_session)
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, detail="Missing token.")

    token = authorization.split(" ")[1]

    try:
        token_row = session.exec(select(Token).where(Token.token == token)).one()
    except NoResultFound:
        raise HTTPException(401, detail="Invalid token.")

    user: User = session.get(User, token_row.user_id) # noqa
    if not user:
        raise HTTPException(404, detail="User not found.")
    return user
