
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app.database.connection import SessionFactory
from app.auth.models import User

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