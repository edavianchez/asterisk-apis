from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Ami(BaseModel):
    """
    Configuration for Asterisk Manager Interface (AMI).
    """
    host: str = "localhost"
    port: int = 5038
    username: str = "admin"
    password: str = "password"
    # use_ssl: bool = False


class Ari(BaseModel):
    """
    Configuration for Asterisk REST Interface (ARI).
    """
    host: str = "localhost"
    port: int = 8088
    username: str = "admin"
    password: str = "password"


class Asterisk(BaseModel):
    """
    Configuration for Asterisk connection.
    """
    ami: Ami
    ari: Ari


class Settings(BaseSettings):
    """
    Application settings using Pydantic for configuration management.
    """
    model_config = SettingsConfigDict(env_nested_delimiter='__')

    debug: bool = False
    asterisk: Asterisk


settings = Settings()  # Instantiate the settings object
