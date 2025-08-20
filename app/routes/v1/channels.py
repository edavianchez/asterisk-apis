from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from pydantic import BaseModel
from app.dependencies import get_conn_manager
from app.services.connections import ConnectionManager

router = APIRouter()

class HangupChannelRequest(BaseModel):
    channel: str

    class Config:
        json_schema_extra = {
            "example": {
                "extension": "1001"
            }
        }

@router.post("/channel/hangup-by-extension")
async def hangup_by_extension(
    req: HangupChannelRequest,
    conn_manager: Annotated[ConnectionManager, Depends(get_conn_manager)]
):
    """
    Cuelga el canal en estado 'Up' asociado a una extensión.
    """
    try:
        channels_response = await conn_manager.ami_manager.send_action({
            "Action": "CoreShowChannels"
        })

        channels = channels_response.get("Events", [])

        active_channels = [
            ch for ch in channels
            if ch.get("CallerIDNum") == req.extension and ch.get("ChannelStateDesc") == "Up"
        ]

        if not active_channels:
            raise HTTPException(status_code=404, detail="No se encontró canal en llamada para esa extensión")

        channel_to_hangup = active_channels[0]["Channel"]

        result = await conn_manager.ami_manager.send_action({
            "Action": "Hangup",
            "Channel": channel_to_hangup
        })

        return {
            "status": "success",
            "message": f"Se colgó la llamada de la extensión {req.extension}",
            "data": {
                "channel": channel_to_hangup
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al colgar el canal: {str(e)}")