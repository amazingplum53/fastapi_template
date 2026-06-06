from fastapi import FastAPI, status

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


@app.get("/")
async def root():

    engine = create_engine(settings.DATABASE["URL"], pool_pre_ping=True)

    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar_one()

    return {"ok": True, "result": result}

@app.get("/health")
async def health():
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    