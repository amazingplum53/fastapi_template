from multiprocessing import cpu_count
import uvicorn
from bootstrap import bootstrap

bootstrap()

from app import settings

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