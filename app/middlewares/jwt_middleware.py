from typing import Callable, Awaitable

from fastapi import Request, status, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.jwt import verify_token


class JWTMiddleware(BaseHTTPMiddleware):
    """Middleware de autorización para el acceso a las rutas"""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        if request.url.path.startswith("/api"):
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith('Bearer '):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Authorization header is missing"
                )
            _, token = auth_header.split()
            payload = verify_token(token)
            request.state.auth_user = payload
        response = await call_next(request)
        return response
