
from pathlib import Path
import os
import ast
from sqlalchemy.engine import URL


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

DATABASE = ast.literal_eval(os.environ["DATABASE"])

if "HOST" not in DATABASE:
    DATABASE["HOST"] = os.environ.get("DB_HOST")

DATABASE["URL"] = URL.create(
    drivername="postgresql+psycopg",
    username=DATABASE["USERNAME"],
    host=DATABASE["HOST"],
    port=DATABASE["PORT"],
    database=DATABASE["NAME"],
    password=os.environ["DB_PASSWORD"] 
    if STACK != "local" 
    else DATABASE["PASSWORD"],
)
