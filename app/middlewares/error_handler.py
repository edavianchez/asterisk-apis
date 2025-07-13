from typing import Callable, Awaitable

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.config import settings

logger = settings.logger


class ErrorHandler(BaseHTTPMiddleware):
    """Middleware para la captura y retorno de errores sobre la respuesta json"""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            logger.error(e.__traceback__)
            return JSONResponse(
                content={"error": str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
