from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer

from app.core.config import settings
from app.middlewares.error_handler import ErrorHandler
from app.middlewares.jwt_middleware import JWTMiddleware
from app.routes.routes import api_router_v1, ws_router_v1
from app.dependencies import lifespan


app = FastAPI(title="Asterisk-APIs", lifespan=lifespan)
if not settings.debug:
    app.docs_url = None
    app.openapi_url = None
    app.redoc_url = None
app.add_middleware(ErrorHandler)
#app.add_middleware(JWTMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
bearer_scheme = HTTPBearer()
app.include_router(
    api_router_v1,
    prefix="/api",
    dependencies=[Depends(bearer_scheme)]
)
app.include_router(
    ws_router_v1,
    prefix="/ws",
    # dependencies=[Depends(bearer_scheme)]
)


@app.get("/")
async def root():
    return {"message": "Welcome to Asterisk APIs"}
