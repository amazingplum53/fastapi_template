import os
import sys

STACK = os.getenv("STACK", "local")
print(f"Using {STACK} env file")

os.environ["PROJECT_NAME"] = "fastapi_template"

sys.path.append(f"/server/{os.environ["PROJECT_NAME"]}/")

from utils.keys import handle_secrets
from utils.variables import load_variables

load_variables(STACK)

handle_secrets(STACK)

from fastapi_template import settings

