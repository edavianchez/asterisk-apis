from pydantic import BaseModel, Field


class Channel(BaseModel):
    name: str = Field(..., alias="channel")
    state: int = Field(..., alias="channelstate")
    state_desc: str = Field(..., alias="channelstatedesc")
    connected_line_name: str = Field(..., alias="connectedlinename")
    connected_line_num: str = Field(..., alias="connectedlinenum")
    context: str = Field(..., alias="context")
    duration: str = Field(..., alias="duration")

    class Config:
        # Permite inicializar usando los nombres de campo de Pydantic o los alias
        populate_by_name = True
        # Ignora cualquier campo en el mensaje de Panoramisk que no esté en este modelo
        extra = "ignore"
