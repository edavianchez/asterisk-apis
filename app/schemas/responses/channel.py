from pydantic import BaseModel, Field, computed_field
from typing import Optional
from enum import IntEnum


class ChannelState(IntEnum):
    """Mapea estados numéricos de canales Asterisk a texto"""
    DOWN = 0               # Canal inactivo/colgado
    RESERVED = 1           # Reservado (uso interno)
    OFFHOOK = 2            # Descolgado (inicio llamada)
    DIALING = 3            # Marcando número
    RING = 4               # Recibiendo señal de ring
    RINGING = 5            # Teléfono sonando (llamada entrante)
    UP = 6                 # Llamada activa/establecida
    BUSY = 7               # Ocupado (tono de busy)
    DIALING_OFFHOOK = 8    # Marcando después de descolgar
    PRERING = 9            # Información previa al ring

    @property
    def friendly_name(self):
        """Devuelve descripción amigable"""
        names = {
            0: "Inactivo",
            1: "Reservado (interno)",
            2: "Teléfono descolgado",
            3: "Marcando número",
            4: "Recibiendo señal de ring",
            5: "Teléfono sonando",
            6: "Llamada en progreso",
            7: "Línea ocupada",
            8: "Marcando (descolgado)",
            9: "Pre-ring"
        }
        return names[self.value]


class Channel(BaseModel):
    account_code: str = Field(..., alias='AccountCode')
    channel: str = Field(..., alias='Channel')
    channel_state: ChannelState = Field(..., alias='ChannelState')
    state_description: str = Field(..., alias='ChannelStateDesc')
    caller_id_name: str = Field(..., alias="CallerIDName")
    caller_id: str = Field(..., alias='CallerIDNum')
    conected_line_name: str = Field(..., alias="ConnectedLineName")
    extension: str = Field(..., alias='Exten')
    context: str = Field(..., alias='Context')
    duration: str = Field(..., alias='Duration')
    linked_id: str = Field(..., alias='Linkedid')
    unique_id: str = Field(..., alias='Uniqueid')
    application: Optional[str] = Field(None, alias='Application')
    priority: str = Field(..., alias="Priority")
    conected_line_num: str = Field(..., alias="ConnectedLineNum")

    @computed_field
    def channel_state_name(self) -> str:
        return ChannelState(self.channel_state).friendly_name

    class Config:
        # Permite inicializar usando los nombres de campo de Pydantic o los alias
        populate_by_name = True
        # Ignora cualquier campo en el mensaje de Panoramisk que no esté en este modelo
        extra = "ignore"
