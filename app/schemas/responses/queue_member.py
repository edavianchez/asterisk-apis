from pydantic import BaseModel, Field, computed_field, field_validator, ValidationInfo
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


class AgentState(IntEnum):
    UNKNOWN = 0         # Estado desconocido
    AVAILABLE = 1       # Alias para estado disponible
    ON_CALL = 2         # Alias para estado en llamada
    CALLING = 3         # Alias para estado llamando
    IN_PAUSE = 4        # Alias para estado en pausa
    DISCONNECTED = 5    # Alias para estado no disponible
    ON_HOLD = 6         # Alias para estado en espera

    @property
    def friendly_name(self):
        names = {
            1: "Disponible",
            2: "En llamada",
            3: "Llamando",
            4: "En pausa",
            5: "Desconectado",
            6: "On Hold"
        }
        return names[self.value]


class QueueMemberBase(BaseModel):
    """
    Modelo Pydantic para el evento 'QueueMember' de Panoramisk.
    """
    location: str = Field(..., alias='location')
    name: str = Field(..., alias='name')
    paused: bool = Field(..., alias='paused')
    paused_reason: str = Field(..., alias='pausedreason')
    queue: str = Field(..., alias='queue')
    status: int = Field(..., alias='status')
    campaigns: list[str] = []

    @computed_field()
    def status_name(self) -> str:
        """Devuelve el nombre del estado como texto"""
        return AgentState(self.status).friendly_name

    @computed_field()
    def campaign(self) -> str:
        """Devuelve el nombre del estado como texto"""
        return self.queue.replace("Q", "")

    @field_validator("location")
    def parse_location(cls, value):
        return value.replace("SIP/", "ext. ")

    @field_validator("paused_reason")
    def parse_paused_reason(cls, value):
        return "N/A" if value == "" else value

    @field_validator("status", mode="after")
    def set_status(cls, v, values):
        match v:
            case MemberState.UNAVAILABLE.value:
                v = AgentState.DISCONNECTED.value
            case MemberState.NOT_INUSE.value:
                v = AgentState.AVAILABLE.value
            case MemberState.INUSE.value | MemberState.BUSY.value:
                v = AgentState.ON_CALL.value
            case MemberState.RINGING.value | MemberState.RINGINUSE.value:
                v = AgentState.CALLING.value
            case MemberState.ONHOLD.value:
                v = AgentState.ON_HOLD.value
            case MemberState.INVALID.value | MemberState.UNKNOWN.value:
                v = AgentState.UNKNOWN.value
            case _:
                v = AgentState.UNKNOWN.value
        return AgentState.IN_PAUSE.value if values.data["paused"] else v

    class Config:
        # Permite inicializar usando los nombres de campo de Pydantic o los alias
        populate_by_name = True
        # Ignora cualquier campo en el mensaje de Panoramisk que no esté en este modelo
        extra = "ignore"


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
