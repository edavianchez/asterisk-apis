import logging
from fastapi import FastAPI

from app.routes.routes import api_router_v1
from app.services.ami import lifespan
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(title="Asterisk-APIs", lifespan=lifespan)
if not settings.debug:
    app.docs_url = None
    app.openapi_url = None
    app.redoc_url = None
app.include_router(api_router_v1, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Welcome to Asterisk APIs"}
