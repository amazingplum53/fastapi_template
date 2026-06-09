from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/auth", tags=["auth"])

templates = Jinja2Templates(directory="app/auth/templates")


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request},
    )


@router.get("/signup")
def signup_page(request: Request):
    return templates.TemplateResponse(
        "signup.html",
        {"request": request},
    )


@router.get("/success")
def signup_page(request: Request):
    return templates.TemplateResponse(
        "success.html",
        {"request": request},
    )