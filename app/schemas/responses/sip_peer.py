from pydantic import BaseModel, Field
from typing import Optional


class SipPeer(BaseModel):
    """
    Modelo Pydantic para el evento 'SIPPeerEntry' de Panoramisk.
    """
    objectname: str = Field(..., alias='objectname')
    ipaddress: Optional[str] = Field(None, alias='ipaddress')
    ipport: Optional[int] = Field(None, alias='ipport')
    status: str = Field(..., alias='status')

    class Config:
        # Permite inicializar usando los nombres de campo de Pydantic o los alias
        populate_by_name = True
        # Ignora cualquier campo en el mensaje de Panoramisk que no esté en este modelo
        extra = "ignore"
