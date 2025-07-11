from fastapi import HTTPException


class QueueException(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


class QueueNotFoundException(QueueException):
    def __init__(self, queue_name: str):
        super().__init__(
            status_code=404,
            detail=f"Queue '{queue_name}' not found"
        )


class NoQueuesFoundException(QueueException):
    def __init__(self):
        super().__init__(status_code=404, detail="No queues found")


class MemberNotFoundException(QueueException):
    def __init__(self, queue_name: str):
        super().__init__(
            status_code=404,
            detail=f"No members found for queue '{queue_name}'"
        )


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


class ChannelException(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


class NoChannelsFoundException(ChannelException):
    def __init__(self):
        super().__init__(status_code=404, detail="No channels found")


class ChannelNotFoundException(ChannelException):
    def __init__(self, channel_name: str):
        super().__init__(
            status_code=404,
            detail=f"Channel '{channel_name}' not found"
        )
