from typing import Optional
from app.schemas.responses.queue_member import QueueMemberBase


class MemberStatusTable(QueueMemberBase):
    duration: Optional[str] = "N/A"
    ip_address: Optional[str] = "N/A"
    phone_number: Optional[str] = "N/A"
    device_status: Optional[str] = "N/A"
    call_status: Optional[str] = "N/A"

    class Config:
        # Permite inicializar usando los nombres de campo de Pydantic o los alias
        populate_by_name = True
        # Ignora cualquier campo en el mensaje de Panoramisk que no esté en este modelo
        extra = "ignore"
