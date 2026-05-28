from multiprocessing import cpu_count
import uvicorn


def bootstrap():

    import sys
    import os

    STACK = os.getenv("STACK", "local")
    print(f"Using {STACK} env file")

    from utils.keys import handle_secrets
    from utils.variables import load_variables

    load_variables(STACK)

    handle_secrets(STACK)

bootstrap()

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