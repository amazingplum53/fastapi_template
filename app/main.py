from fastapi import FastAPI, status
from fastapi import Request, HTTPException
from fastapi.responses import FileResponse

from starlette.responses import Response
from starlette.staticfiles import StaticFiles

from sqlalchemy import create_engine, text

from pathlib import Path

from app.middleware import MIDDLEWARE
from app import settings
from app.auth.api import router as auth_api_router
from app.auth.pages import router as auth_pages_router

app = FastAPI(
    middleware=MIDDLEWARE,
    debug=settings.DEBUG
)

app.include_router(auth_api_router)
app.include_router(auth_pages_router)

if settings.STATIC_URL == "/static":
    static_dir = Path(settings.BASE_DIR) / "static"
    app.mount(
        "/static",
        StaticFiles(directory=static_dir, html=False),
        name="static",
    )


@app.get("/health")
async def health():
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/{path:path}")
async def frontend(request: Request, path: str):

    FRONTEND_ROUTES = {
        "/auth": [
            "/signup",
            "/login",
        ],
    }

    paths = []

    for root_path, path_list in FRONTEND_ROUTES.items():
        for child_path in path_list:
            paths.append(f"{root_path}{child_path}")

    if f"/{path}" not in FRONTEND_ROUTES:
        raise HTTPException(status_code=404)

    return templates.TemplateResponse(
        "index.html",
        {"request": request},
    )


@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return FileResponse(
        settings.BASE_DIR + "/static/404.html",
        status_code=404,
        media_type="text/html",
    )