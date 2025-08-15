from fastapi import APIRouter

from app.routes.v1 import websockets

api_router_v1 = APIRouter(prefix="/v1")

ws_router_v1 = APIRouter(prefix="/v1")
ws_router_v1.include_router(
    websockets.router,
    tags=["WebSockets"]
)
