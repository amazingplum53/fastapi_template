# app/routes/auth.py

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.auth.models import User
from utils.user import hash_password, authenticate_user


router = APIRouter(prefix="/auth", tags=["auth"])


class SignupRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/signup")
def signup(data: SignupRequest, db_session: Session = Depends(get_db)):
    existing_user = (
        db_session.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return {
        "id": str(user.id),
        "email": user.email,
    }


@router.post("/login")
def login(data: LoginRequest, db_session: Session = Depends(get_db)):
    user = authenticate_user(data.email, data.password, db_session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return {
        "message": "Login successful",
        "id": str(user.id),
        "email": user.email,
    }