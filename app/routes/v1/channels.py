from typing import Annotated
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status, Body
from app.dependencies import get_conn_manager
from app.services.connections import ConnectionManager
from app.schemas.requests.hangup_channel_request import HangupChannelRequest

router = APIRouter()


@router.post("/channel/hangup-by-channel-sip")
async def hangup_by_channel_sip(
    req: Annotated[HangupChannelRequest, Body()],
    conn_manager: Annotated[ConnectionManager, Depends(get_conn_manager)]
) -> JSONResponse:
    """
    Cuelga el canal en estado 'Up' asociado a un asesor.
    """
    try:
        channels = await conn_manager.ami_manager.send_action({
            "Action": "CoreShowChannels"
        })

        await conn_manager.ami_manager.send_action({
            "Action": "Hangup",
            "Channel": req.channel_sip
        })

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "success",
                "message": f"Se colgó la llamada de la extensión {req.channel_sip}",
            }
        )
    except Exception as e:
            return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "detail": f"Error al colgar el canal: {str(e)}"
            }
         )