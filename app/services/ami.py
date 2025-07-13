import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status as http_status
from panoramisk import Manager

from app.core.config import settings

logger = settings.logger
ami = settings.asterisk.ami


@asynccontextmanager
async def lifespan(app: FastAPI):
    manager = Manager(
        host=ami.host,
        port=ami.port,
        username=ami.username,
        secret=ami.password.get_secret_value(),
    )
    try:
        await manager.connect()
        app.state.manager = manager
        logger.info("Connected to Asterisk AMI")
        yield
    except Exception as e:
        logger.error(f"Failed to connect to Asterisk AMI: {e}")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not connect to Asterisk AMI"
        )
    finally:
        if manager:
            manager.close()
            logger.info("Disconnected from Asterisk AMI")
