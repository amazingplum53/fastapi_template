from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware import Middleware

from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

import settings


MIDDLEWARE = []

MIDDLEWARE.append(
    Middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)
)

MIDDLEWARE.append(
    Middleware(ProxyHeadersMiddleware, trusted_hosts="*")
)

MIDDLEWARE.append(
    Middleware(
        CORSMiddleware,
        allow_origins=settings.CSRF_TRUSTED_ORIGINS,
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Authorization", "Content-Type", "Accept"],
        max_age=86400,
    )
)
