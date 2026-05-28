from pwdlib import PasswordHash

from app.database.connection import SessionFactory
from app.database.models import User


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(input_password: str, hashed_password: str) -> str:
    password_hash = PasswordHash.recommended()
    return password_hash.verify(password, user.hashed_password)


def authenticate_user(email: str, password: str):

    db_session = SessionFactory()

    user = db_session.query(User).filter(User.email == email).first()

    if not user:
        return None


    if not verify_password(password, user.hashed_password):
        return None

    return user