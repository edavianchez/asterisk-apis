from pydantic import BaseModel, Field, field_validator


class Hangup(BaseModel):
    location: str = Field(..., alias="channel")

    @field_validator("location")
    def parce_channel(cls, value: str):
        return value.split("-")[0].replace("SIP/", "ext. ")

    class Config:
        # Permite inicializar usando los nombres de campo de Pydantic o los alias
        populate_by_name = True
        # Ignora cualquier campo en el mensaje de Panoramisk que no esté en este modelo
        extra = "ignore"
