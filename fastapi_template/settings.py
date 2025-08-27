
from pathlib import Path
import os
import json

PROJECT_NAME = os.environ['PROJECT_NAME']
BASE_DIR = f'/server/{PROJECT_NAME}'

STACK = os.getenv("STACK", "local")

# Import variables from json file
with open(f"{BASE_DIR}/{PROJECT_NAME}/env/{STACK}.json", "r") as f:
    ENV_VARIABLES = json.loads(f.read())

    for name, value in ENV_VARIABLES.items():
        globals()[key] = value

if STACK == "local":
    protocol = "http://"
else:
    protocol = "https://"

CSRF_TRUSTED_ORIGINS = [
    protocol + domain
    for domain in ALLOWED_HOSTS
]

APPEND_SLASH = True

