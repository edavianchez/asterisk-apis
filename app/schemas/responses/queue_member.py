from pydantic import BaseModel, Field
from typing import Optional


class QueueMember(BaseModel):
    """
    Modelo Pydantic para el evento 'QueueMember' de Panoramisk.
    """
    queue: str = Field(..., alias='queue')
    name: str = Field(..., alias='name')
    location: str = Field(..., alias='location')
    membership: str = Field(..., alias='membership')
    penalty: str = Field(..., alias='penalty')
    callstaken: str = Field(..., alias='callstaken')
    lastcall: str = Field(None, alias='lastcall')
    lastpause: str = Field(None, alias='lastpause')
    logintime: str = Field(None, alias='logintime')
    incall: str = Field(None, alias='incall')
    status: str = Field(..., alias='status')
    paused: str = Field(..., alias='paused')
    pausedreason: str = Field(None, alias='pausedreason')
    wrapuptime: str = Field(None, alias='wrapuptime')

    class Config:
        # Permite inicializar usando los nombres de campo de Pydantic o los alias
        populate_by_name = True
        # Ignora cualquier campo en el mensaje de Panoramisk que no esté en este modelo
        extra = "ignore"
