
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app.database.connection import SessionFactory
from app.auth.models import User

import os
from datetime import datetime, timedelta, timezone
from uuid import UUID
import jwt

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(input_password: str, hashed_password: str) -> str:
    return password_hash.verify(input_password, hashed_password)


def authenticate_user(email: str, password: str, session: Session):

    user = session.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"

def create_access_token(user_id: UUID):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    return jwt.encode(
        {
            "user_id": str(user_id),
            "exp": expire,
        }, 
        os.environ["SECRET_KEY"], 
        algorithm=ALGORITHM
    )


def decode_access_token(token: str):
    try:
        return jwt.decode(
            token,
            os.environ["SECRET_KEY"],
            algorithm=ALGORITHM,
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")