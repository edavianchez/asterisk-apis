from fastapi import APIRouter, status as http_status
from panoramisk import Manager
from typing import Annotated, List

from app.dependencies import AMIManager
from app.schemas.responses.channel import Channel
from app.services.channels import Channels
from app.core.exceptions import NoChannelsFoundException


router = APIRouter(
    responses={
        http_status.HTTP_404_NOT_FOUND: {
            "description": "Not Found",
            "content": {"application/json": {"example": {"detail": "Not Found"}}},
        },
    },
)


@router.get("/", status_code=http_status.HTTP_200_OK, response_model=List[Channel])
async def list(manager: Annotated[Manager, AMIManager]):
    """
    List all channels.
    """
    response = await manager.send_action({'Action': 'CoreShowChannels'})
    channels_info = Channels.map(response)
    if not channels_info:
        raise NoChannelsFoundException()
    return channels_info
