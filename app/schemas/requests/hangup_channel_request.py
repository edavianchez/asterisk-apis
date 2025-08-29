from pydantic import BaseModel

class HangupChannelRequest(BaseModel):
    channel_sip: str

    class Config:
        json_schema_extra = {
            "example": {
                "channel_sip": "SIP/1001"
            }
        }