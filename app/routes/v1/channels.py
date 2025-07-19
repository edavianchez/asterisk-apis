from fastapi import APIRouter, status as http_status, Depends
from panoramisk import Manager
from typing import Annotated, List

from app.dependencies import get_conn_manager
from app.schemas.responses.channel import Channel
from app.services.channels import Channels
from app.exceptions.channel_exceptions import NoChannelsFoundException
from app.services.connections import ConnectionManager


router = APIRouter(
    responses={
        http_status.HTTP_404_NOT_FOUND: {
            "description": "Not Found",
            "content": {"application/json": {"example": {"detail": "Not Found"}}},
        },
    },
)


@router.get("/", status_code=http_status.HTTP_200_OK, response_model=List[Channel])
async def list(conn_manager: Annotated[ConnectionManager, Depends(get_conn_manager)]):
    """
    List all channels.
    """
    response = await conn_manager.ami_manager.send_action({'Action': 'CoreShowChannels'})
    channels_info = Channels.map(response)
    if not channels_info:
        raise NoChannelsFoundException()
    return channels_info
