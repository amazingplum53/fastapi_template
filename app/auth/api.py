from fastapi import APIRouter, HTTPException, status, Depends, Form
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.auth.models import User
from utils.user import hash_password, authenticate_user


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
def signup(
    email: EmailStr = Form(...),
    password: str = Form(...),
    db_session: Session = Depends(get_db),
):
    existing_user = (
        db_session.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = User(
        email=email,
        hashed_password=hash_password(password),
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return {
        "id": str(user.id),
        "email": user.email,
    }


@router.post("/login")
def login(
    email: EmailStr = Form(...),
    password: str = Form(...),
    db_session: Session = Depends(get_db),
):
    user = authenticate_user(email, password, db_session)

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