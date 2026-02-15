from fastapi import Depends, Header
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from starlette.exceptions import HTTPException
import bcrypt
import hashlib

from db.database import get_session
from models.token import Token
from models.user import User

def hash_password(password: str) -> str:
    """Хеширование пароля с помощью bcrypt + SHA-256"""
    # SHA-256 для снятия ограничения длины
    pre_hashed = hashlib.sha256(password.encode('utf-8')).digest()
    # bcrypt хеширование
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pre_hashed, salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """Проверка пароля"""
    # Тот же SHA-256 для проверяемого пароля
    pre_hashed = hashlib.sha256(password.encode('utf-8')).digest()
    # Проверка через bcrypt
    return bcrypt.checkpw(
        pre_hashed, 
        hashed_password.encode('utf-8')
    )

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