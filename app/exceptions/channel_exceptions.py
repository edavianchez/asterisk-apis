from fastapi import HTTPException


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
