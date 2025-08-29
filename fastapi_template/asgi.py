from multiprocessing import cpu_count
import os
import uvicorn

from secret.keys import handle_secrets

STACK = os.getenv("STACK", "local")
print(f"Using {STACK} env file")

os.environ["PROJECT_NAME"] = "fastapi_template"

handle_secrets(STACK)

import settings

no_of_workers = 1 if settings.DEBUG else cpu_count()

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0",
        port=8000,
        workers=no_of_workers,
        timeout_keep_alive=5,
        log_level="info",
        reload=settings.DEBUG
    )