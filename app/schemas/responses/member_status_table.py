from typing import Optional
from app.schemas.responses.queue_member import QueueMemberBase
from pydantic import computed_field, field_validator, ValidationInfo
from datetime import datetime


class MemberStatusTable(QueueMemberBase):
    duration: Optional[str] = "N/A"
    ip_address: Optional[str] = "N/A"
    phone_number: Optional[str] = "N/A"
    device_status: Optional[str] = "N/A"
    call_status: Optional[str] = "N/A"
    hold_start_at: Optional[str | None] = None
    paused_start_at: Optional[str | None] = None
    is_connected: bool = True
    last_connection: Optional[str] = "N/A"

    @computed_field()
    def hold_time(self) -> str:
        hold_time = "N/A"
        if self.hold_start_at:
            start_at = float(self.hold_start_at)
            start_at = datetime.fromtimestamp(start_at)
            now = datetime.now()
            diff = now - start_at
            hours, remainder = divmod(diff.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            hold_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return hold_time

    @computed_field()
    def paused_time(self) -> str:
        pause_time = "N/A"
        if self.paused_start_at and self.paused:
            start_at = float(self.paused_start_at)
            start_at = datetime.fromtimestamp(start_at)
            now = datetime.now()
            diff = now - start_at
            hours, remainder = divmod(diff.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            pause_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return pause_time

    @field_validator("paused_start_at", mode="after")
    @classmethod
    def set_paused_start_at_None(cls, v, values):
        return None if not values.data["paused"] else v

    class Config:
        # Permite inicializar usando los nombres de campo de Pydantic o los alias
        populate_by_name = True
        # Ignora cualquier campo en el mensaje de Panoramisk que no esté en este modelo
        extra = "ignore"
