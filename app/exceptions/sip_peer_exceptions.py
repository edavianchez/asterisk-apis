from fastapi import HTTPException


class SipPeerException(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


class SipPeerNotFoundException(SipPeerException):
    def __init__(self, peer_name: str):
        super().__init__(
            status_code=404,
            detail=f"SIP peer '{peer_name}' not found"
        )


class NoSipPeersFoundException(SipPeerException):
    def __init__(self):
        super().__init__(status_code=404, detail="No SIP peers found")
