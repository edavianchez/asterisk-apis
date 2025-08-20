from typing import Optional
from pydantic import computed_field, field_validator, Field, BaseModel
from datetime import datetime, timedelta
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
    """Map interno de estados de los agentes"""
    UNKNOWN = 0         # Estado desconocido
    AVAILABLE = 1       # Alias para estado disponible
    ON_CALL = 2         # Alias para estado en llamada
    CALLING = 3         # Alias para estado llamando
    IN_PAUSE = 4        # Alias para estado en pausa
    DISCONNECTED = 5    # Alias para estado no disponible
    ON_HOLD = 6         # Alias para estado en espera

    @property
    def friendly_name(self):
        """Nombre amigable del estado"""
        names = {
            1: "Disponible",
            2: "En llamada",
            3: "Llamando",
            4: "En pausa",
            5: "Desconectado",
            6: "On Hold"
        }
        return names[self.value]


class QueueMember(BaseModel):
    """Modelo de agentes"""
    location: str = Field(..., alias='location')
    name: str = Field(..., alias='name')
    paused: bool = Field(..., alias='paused')
    paused_reason: str = Field(..., alias='pausedreason')
    queue: str = Field(..., alias='queue')
    duration: Optional[str] = "N/A"
    ip_address: Optional[str] = "N/A"
    phone_number: str = Field(default="N/A")
    device_status: Optional[str] = "N/A"
    call_status: Optional[str] = "N/A"
    hold_start_at: Optional[str | None] = None
    paused_start_at: Optional[str | None] = None
    is_connected: bool = True
    last_connection: Optional[str] = "N/A"
    hold_time_accumulator: str = "00:00:00"
    last_hold_phone_number: str = "N/A"
    status: int = Field(..., alias='Status')
    campaigns: list[str] = []

    @field_validator("paused_start_at", mode="after")
    def set_paused_start_at_None(cls, v, values):
        """Restablece el inicio de la pausa"""
        return (
            None
            if not values.data["paused"] or values.data["paused_reason"] == "LLamada Saliente"
            else v
        )

    @field_validator("status", mode="after")
    def parse_status(cls, v, values):
        """Establece el estado del agente"""
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
        if values.data["paused"]:
            if v != AgentState.ON_HOLD.value:
                v = AgentState.IN_PAUSE.value
                if (
                    values.data["paused_reason"] == "llamada saliente"
                    and values.data["call_status"] != "N/A"
                ):
                    v = AgentState.ON_CALL.value
        return v

    @field_validator("location")
    def parse_location(cls, value):
        """Cambia el texto de localización"""
        return value.replace("SIP/", "ext. ")

    @field_validator("paused_reason")
    def parse_paused_reason(cls, value):
        """Establece en N/A si no hay razón de pausa"""
        return "N/A" if value == "" else value

    @computed_field()
    def hold_time(self) -> str:
        """Calcula el tiempo de hold de la llamada"""
        hold_time = datetime.strptime(self.hold_time_accumulator, "%H:%M:%S")
        hold_time_delta = timedelta(
            hours=hold_time.hour,
            minutes=hold_time.minute,
            seconds=hold_time.second
        )
        if self.hold_start_at:
            start_at = float(self.hold_start_at)
            start_at = datetime.fromtimestamp(start_at)
            now = datetime.now()
            diff = now - start_at
            total_hold_time = hold_time_delta + diff
        else:
            total_hold_time = hold_time_delta

        hours, remainder = divmod(total_hold_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    @computed_field()
    def paused_time(self) -> str:
        """Calcula el tiempo en pausa"""
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

    @computed_field()
    def extension(self) -> str:
        """Extensión numérica"""
        return self.location.replace("ext. ", "")

    @computed_field()
    def status_name(self) -> str:
        """Devuelve el nombre del estado como texto"""
        return AgentState(self.status).friendly_name

    @computed_field()
    def campaign(self) -> str:
        """Devuelve el nombre del estado como texto"""
        return self.queue.replace("Q", "")

    def validate_status(self):
        """Verifica el estado de del agente según la pausa"""
        if self.paused:
            if self.status != AgentState.ON_HOLD.value:
                self.status = AgentState.IN_PAUSE.value
                if (
                    self.paused_reason == "llamada saliente"
                    and self.call_status != "N/A"
                ):
                    self.status = AgentState.ON_CALL.value

    class Config:
        # Permite inicializar usando los nombres de campo de Pydantic o los alias
        populate_by_name = True
        # Ignora cualquier campo en el mensaje de Panoramisk que no esté en este modelo
        extra = "ignore"
