import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status as http_status
from panoramisk import Manager

from app.core.config import settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    manager = Manager(
        host=settings.asterisk.ami.host,
        port=settings.asterisk.ami.port,
        username=settings.asterisk.ami.username,
        secret=settings.asterisk.ami.password.get_secret_value(),
    )
    try:
        await manager.connect()
        app.state.manager = manager
        logger.info("*"*50)
        logger.info(
            f"* Conectado a Asterisk AMI en {manager.config["host"]}:{manager.config["port"]} *"
        )
        logger.info("*"*50)
        yield
    except Exception as e:
        logger.info("*"*50)
        logger.error(f"Error connecting to Asterisk AMI: {e}")
        logger.info("*"*50)
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not connect to Asterisk AMI"
        )
    finally:
        if manager:
            manager.close()
            logger.info("*"*50)
            logger.info("Disconnected from Asterisk AMI")
            logger.info("*"*50)
