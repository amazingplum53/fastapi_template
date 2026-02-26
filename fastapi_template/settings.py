
from pathlib import Path
import os
import ast

PROJECT_NAME = os.environ['PROJECT_NAME']
BASE_DIR = f'/server/{PROJECT_NAME}'
STACK = os.getenv("STACK", "local")

ALLOWED_HOSTS = ast.literal_eval(os.environ["ALLOWED_HOSTS"])
PROTOCOL = os.environ["PROTOCOL"]

DEBUG = os.environ["PROTOCOL"]

CSRF_TRUSTED_ORIGINS = [
    PROTOCOL + "://" + domain
    for domain in ALLOWED_HOSTS
]

if "STATIC_URL" in os.environ and os.environ["STATIC_URL"] is not None:
    STATIC_URL = os.environ["STATIC_URL"]
else:
    STATIC_URL = "/static"

    