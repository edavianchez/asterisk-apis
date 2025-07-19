from fastapi import APIRouter, status as http_status, Depends
from typing import Annotated, List
from panoramisk import Manager

from app.dependencies import get_conn_manager
from app.services.sip_peers import SipPeers
from app.services.connections import ConnectionManager
from app.schemas.responses.sip_peer import SipPeer
from app.exceptions.sip_peer_exceptions import NoSipPeersFoundException
from app.exceptions.asterisk_exceptions import AsteriskTypeErrorException

router = APIRouter(
    responses={
        http_status.HTTP_404_NOT_FOUND: {
            "description": "Not Found",
            "content": {"application/json": {"example": {"detail": "Not Found"}}},
        },
    },
)


@router.get("/", status_code=http_status.HTTP_200_OK, response_model=List[SipPeer])
async def list_sip_peers(conn_manager: Annotated[ConnectionManager, Depends(get_conn_manager)]):
    """
    List all SIP peers.
    """
    try:
        response = await conn_manager.ami_manager.send_action({'Action': 'SIPpeers'})
        sip_peers_info = SipPeers.map(response)
        if not sip_peers_info:
            raise NoSipPeersFoundException()
        return sip_peers_info
    except TypeError as e:
        if e == "unhashable type: 'list'":
            raise AsteriskTypeErrorException()
