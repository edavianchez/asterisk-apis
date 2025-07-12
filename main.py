from fastapi import FastAPI

from app.core.error_handlers import queue_exception_handler
from app.core.exceptions import QueueException
from app.core.config import settings
from app.middleware.error_handling import http_error_handler
from app.routes.routes import api_router_v1
from app.services.ami import lifespan


app = FastAPI(title="Asterisk-APIs", lifespan=lifespan)
app.middleware("http")(http_error_handler)
app.add_exception_handler(QueueException, queue_exception_handler)
if not settings.debug:
    app.docs_url = None
    app.openapi_url = None
    app.redoc_url = None
app.include_router(api_router_v1, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Welcome to Asterisk APIs"}
