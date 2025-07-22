from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Optional
from enum import Enum


class SIPPeerStatus(Enum):
    """Estados de dispositivos SIP en Asterisk"""
    UNKNOWN = "Unknown"
    UNREACHABLE = "Unreachable"          # No alcanzable (problemas de red)
    REACHABLE = "Reachable"              # Alcanzable pero no registrado
    LAGGED = "Lagged"                    # Registrado con alta latencia
    REGISTERED = "Registered"            # Correctamente registrado (OK)
    UNREGISTERED = "Unregistered"        # No registrado (pero configurado)
    UNMONITORED = "Unmonitored"          # No monitoreado
    # Fallo de registro (credenciales inválidas)
    FAILED = "Failed"
    PROGRESS = "Progress"                # Registro en progreso
    EXPIRED = "Expired"                  # Registro expirado
    # Estados adicionales comunes
    QUALITY_WARNING = "Quality Warning"  # Problemas de calidad
    OFFLINE = "Offline"                  # Desconectado
    ONLINE = "Online"                    # Conectado

    @classmethod
    def from_asterisk_status(cls, status_str: str):
        """Convierte texto crudo de Asterisk a enum"""
        status_map = {
            "UNREACHABLE": cls.UNREACHABLE,
            "REACHABLE": cls.REACHABLE,
            "LAGGED": cls.LAGGED,
            "OK": cls.REGISTERED,        # Asterisk usa "OK" para registrado
            "UNKNOWN": cls.UNKNOWN,
            "UNMONITORED": cls.UNMONITORED,
            "Progress": cls.PROGRESS,
            "Failed": cls.FAILED,
            "Expired": cls.EXPIRED,
            "": cls.UNKNOWN
        }
        return status_map.get(status_str.strip().upper(), cls.UNKNOWN)


class SipPeer(BaseModel):
    """
    Modelo Pydantic para el evento 'SIPPeerEntry' de Panoramisk.
    """
    objectname: str = Field(..., alias='objectname')
    ipaddress: Optional[str] = Field(None, alias='ipaddress')
    ipport: Optional[int] = Field(None, alias='ipport')
    status: str = Field(..., alias='status')
    # status: SIPPeerStatus = Field(..., alias='status')

    @computed_field
    def status_name(self) -> str:
        return SIPPeerStatus.from_asterisk_status(self.status.split(" ")[0]).value

    @field_validator("objectname")
    def parce_objectname(cls, value):
        return f"ext. {value}"

    class Config:
        # Permite inicializar usando los nombres de campo de Pydantic o los alias
        populate_by_name = True
        # Ignora cualquier campo en el mensaje de Panoramisk que no esté en este modelo
        extra = "ignore"
