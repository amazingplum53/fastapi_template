from multiprocessing import cpu_count
import os
import uvicorn

from main import app
from secret.keys import handle_secrets

STACK = os.getenv("STACK", "local")
print(f"Using {STACK} env file")

os.environ["PROJECT_NAME"] = "fastapi_template"

handle_secrets(STACK)

import settings

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0",
        port=8000,
        workers=cpu_count(),
        timeout_keep_alive=5,
        proxy_headers=True,
        forwarded_allow_ips="*",
        log_level="info",
    )