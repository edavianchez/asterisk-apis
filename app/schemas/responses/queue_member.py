from pydantic import BaseModel, Field, computed_field
from enum import IntEnum


class MemberState(IntEnum):
    """Mapea estados numéricos de Asterisk a texto legible"""
    UNKNOWN = 0
    NOT_INUSE = 1       # Disponible
    INUSE = 2           # En uso (en llamada)
    BUSY = 3            # Ocupado
    INVALID = 4         # Inválido
    UNAVAILABLE = 5     # No disponible
    RINGING = 6         # Llamando
    RINGINUSE = 7       # Recibiendo nueva llamada mientras ya tiene una activa
    ONHOLD = 8          # En espera

    @property
    def friendly_name(self):
        names = {
            0: "Desconocido",
            1: "Disponible",
            2: "En llamada",
            3: "Ocupado",
            4: "Inválido",
            5: "No disponible",
            6: "Llamando",
            7: "Llamando (mientras esta en llamada)",
            8: "En espera"
        }
        return names[self.value]


class QueueMemberBase(BaseModel):
    """
    Modelo Pydantic para el evento 'QueueMember' de Panoramisk.
    """
    location: str = Field(..., alias='location')
    name: str = Field(..., alias='name')
    paused: str = Field(..., alias='paused')
    queue: str = Field(..., alias='queue')
    status: int = Field(..., alias='status')

    @computed_field()
    def status_name(self) -> str:
        """Devuelve el nombre del estado como texto"""
        return MemberState(self.status).friendly_name


class QueueMember(QueueMemberBase):
    """
    Modelo Pydantic para el evento 'QueueMember' de Panoramisk.
    """
    state_interface: str = Field(..., alias='stateinterface')
    membership: str = Field(..., alias='membership')
    penalty: str = Field(..., alias='penalty')
    callstaken: str = Field(..., alias='callstaken')
    lastcall: str = Field(None, alias='lastcall')
    lastpause: str = Field(None, alias='lastpause')
    logintime: str = Field(None, alias='logintime')
    incall: str = Field(None, alias='incall')
    pausedreason: str = Field(None, alias='pausedreason')
    wrapuptime: str = Field(None, alias='wrapuptime')

    class Config:
        # Permite inicializar usando los nombres de campo de Pydantic o los alias
        populate_by_name = True
        # Ignora cualquier campo en el mensaje de Panoramisk que no esté en este modelo
        extra = "ignore"
