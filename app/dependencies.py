import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.services.connections import ConnectionManager

conn_manager = ConnectionManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await conn_manager.start()
    yield
    await conn_manager.close()


async def get_conn_manager() -> ConnectionManager:
    return conn_manager
