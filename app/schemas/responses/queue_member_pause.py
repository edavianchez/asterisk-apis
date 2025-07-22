from pydantic import BaseModel, Field, field_validator


class QueueMemberPause(BaseModel):
    location: str = Field(..., alias="interface")
    paused: bool = Field(..., alias="paused")
    paused_reason: str = Field(..., alias="pausedreason")
    timestamp: str = Field(..., alias="timestamp")
    queue: str = Field(..., alias="queue")

    @field_validator("location")
    def parse_location(cls, value):
        return value.replace("SIP/", "ext. ")

    @field_validator("paused_reason")
    def parce_paused_reason(cls, value):
        return "N/A" if value == "" else value
