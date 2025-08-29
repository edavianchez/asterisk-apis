from fastapi import APIRouter

from app.routes.v1 import websockets, channels

api_router_v1 = APIRouter(prefix="/v1")
api_router_v1.include_router(
    channels.router,
    tags=["Channels"]
)

ws_router_v1 = APIRouter(prefix="/v1")
ws_router_v1.include_router(
    websockets.router,
    tags=["WebSockets"]
)
