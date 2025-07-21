from pydantic import BaseModel, Field


class Hangup(BaseModel):
    location: str = Field(..., alias="channel")

    class Config:
        # Permite inicializar usando los nombres de campo de Pydantic o los alias
        populate_by_name = True
        # Ignora cualquier campo en el mensaje de Panoramisk que no esté en este modelo
        extra = "ignore"
