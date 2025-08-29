from fastapi import FastAPI, status

from starlette.responses import Response
from starlette.staticfiles import StaticFiles

from pathlib import Path

from middleware import MIDDLEWARE
import settings


app = FastAPI(
    middleware=MIDDLEWARE,
    debug=settings.DEBUG
)

if settings.STATIC_URL == "/static":
    static_dir = Path(settings.BASE_DIR) / "static"
    app.mount(
        "/static",
        StaticFiles(directory=static_dir, html=False),
        name="static",
    )


@app.get("/")
async def root():
    return {"ok": True}

@app.get("/health")
async def health():
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    