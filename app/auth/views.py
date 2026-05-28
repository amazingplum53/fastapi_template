# app/routes/auth.py

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr

from app.database.connection import SessionFactory
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
def signup(data: SignupRequest):
    with SessionFactory() as db_session:
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
def login(data: LoginRequest):
    user = authenticate_user(data.email, data.password)

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