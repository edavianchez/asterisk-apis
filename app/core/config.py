from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field


class Ami(BaseModel):
    """
    Configuration for Asterisk Manager Interface (AMI).
    """
    host: str = Field(default="localhost", description="AMI host")
    port: int = Field(default=5038, description="AMI port")
    username: str = Field(..., description="AMI username")
    password: SecretStr = Field(..., description="AMI password")
    # use_ssl: bool = False


class Ari(BaseModel):
    """
    Configuration for Asterisk REST Interface (ARI).
    """
    host: str = Field(default="localhost", description="ARI host")
    port: int = Field(default=8088, description="ARI port")
    username: str = Field(..., description="ARI username")
    password: SecretStr = Field(..., description="ARI password")


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
    app_url: str = Field(
        default="http://localhost:8000",
        description="Base URL of the application"
    )
    asterisk: Asterisk


settings = Settings()  # Instantiate the settings object
