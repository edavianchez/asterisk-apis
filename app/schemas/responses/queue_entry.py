from pydantic import BaseModel, Field, field_validator, computed_field
from typing import Optional


class QueueEntry(BaseModel):
    caller_num: str = Field(..., alias="calleridnum")
    channel: str = Field(..., alias="channel")
    position: int = Field(..., alias="position")
    priority: int = Field(..., alias="priority")
    wait_time: int | str = Field(..., alias="wait")
    queue: str = Field(..., alias="queue")

    @field_validator("channel")
    def parce_channel(cls, value):
        return value.split("-")[0].replace("SIP/", "Call: ")

    @field_validator("wait_time")
    def parce_wait_time(cls, value):
        if ":" not in value:
            value = int(value)
            minutes = value // 60
            seconds = value % 60
            return f"{minutes:02d}:{seconds:02d}"

    @computed_field
    def campaign(self) -> str:
        """Devuelve el nombre de la campaña (cola)"""
        return self.queue.replace("Q", "")

    class Config:
        # Permite inicializar usando los nombres de campo de Pydantic o los alias
        populate_by_name = True
        # Ignora cualquier campo en el mensaje de Panoramisk que no esté en este modelo
        extra = "ignore"
