from pydantic import BaseModel, Field
from typing import Optional


class Queue(BaseModel):
    """
    Modelo Pydantic para el evento 'QueueParams' de Panoramisk.
    """
    queue: str = Field(..., alias='queue')
    strategy: str = Field(..., alias='strategy')
    calls: str = Field(..., alias='calls')
    holdtime: str = Field(..., alias='holdtime')
    talktime: str = Field(..., alias='talktime')
    completed: str = Field(..., alias='completed')
    abandoned: str = Field(..., alias='abandoned')
    servicelevel: str = Field(None, alias='servicelevel')
    servicelevelperf: str = Field(None, alias='servicelevelperf')
    servicelevelperf2: str = Field(None, alias='servicelevelperf2')
    weight: str = Field(None, alias='weight')
    max: str = Field(None, alias='max')

    class Config:
        # Permite inicializar usando los nombres de campo de Pydantic o los alias
        populate_by_name = True
        # Ignora cualquier campo en el mensaje de Panoramisk que no esté en este modelo
        extra = "ignore"
        # o "allow" si quieres capturarlos en un atributo especial __pydantic_extra__
        # o "forbid" si quieres que falle si hay campos no esperados
