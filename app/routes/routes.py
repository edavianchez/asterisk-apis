from fastapi import APIRouter

from app.routes.v1 import queues

api_router_v1 = APIRouter(prefix="/v1")
api_router_v1.include_router(queues.router, prefix="/queues", tags=["Queues"])
