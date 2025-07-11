from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import QueueException


async def queue_exception_handler(request: Request, exc: QueueException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
