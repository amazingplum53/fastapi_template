from fastapi import APIRouter, HTTPException, status, Depends, Form
from pydantic import EmailStr, BaseModel
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.auth.models import User
from utils.user import hash_password, authenticate_user


router = APIRouter(prefix="/auth", tags=["auth"])


class Login(BaseModel):
    email: EmailStr
    password: str

class Signup(BaseModel):
    email: EmailStr
    password: str


@router.post("/signup")
def signup(
    data: Signup,
    db_session: Session = Depends(get_db),
):
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
def login(
    data: Login,
    db_session: Session = Depends(get_db),
):
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


from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

def login_required(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    try:
        payload = decode_access_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db_session.get(User, payload["sub"])

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
    