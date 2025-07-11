from fastapi import APIRouter

from app.routes.v1 import queues, sip_peers, channels

api_router_v1 = APIRouter(prefix="/v1")
api_router_v1.include_router(queues.router, prefix="/queues", tags=["Queues"])
api_router_v1.include_router(
    sip_peers.router,
    prefix="/sip_peers",
    tags=["SIP Peers"]
)
api_router_v1.include_router(
    channels.router,
    prefix="/channels",
    tags=["Channels"]
)
