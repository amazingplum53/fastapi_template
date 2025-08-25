
from pathlib import Path
import os
import json

PROJECT_NAME = os.environ['PROJECT_NAME']
BASE_DIR = f'/server/{PROJECT_NAME}'

SECRET_KEY = os.environ['SECRET_KEY']

STACK = os.getenv("STACK", "local")

with open(f"{BASE_DIR}/{PROJECT_NAME}/env/{STACK}.env.json", "r") as f:
    ENV_VARIABLES = json.loads(f.read())

DEBUG = ENV_VARIABLES["DEBUG"]

ALLOWED_HOSTS = ENV_VARIABLES["ALLOWED_HOSTS"]

if STACK == "local":
    protocol = "http://"
else:
    protocol = "https://"

CSRF_TRUSTED_ORIGINS = [
    protocol + domain
    for domain in ALLOWED_HOSTS
]
    
DOMAIN_NAME = ENV_VARIABLES["DOMAIN_NAME"]

STATIC_URL = ENV_VARIABLES["STATIC_URL"]

APPEND_SLASH = True

