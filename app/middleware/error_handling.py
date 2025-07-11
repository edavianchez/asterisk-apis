import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


async def http_error_handler(request: Request, call_next):
    """
    Handles HTTP errors.
    """
    try:
        return await call_next(request)
    except Exception as e:
        logger.exception(f"Unhandled exception for request {request.url}: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal Server Error"},
        )
