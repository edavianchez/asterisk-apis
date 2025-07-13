import logging
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field
from app.core.logger import setup_logger

# Call setup_logger to configure the root logger
setup_logger()


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


class JwtConfig(BaseModel):
    """
    Configuration for JWT authentication.
    """
    private_key: str = Field(..., description="Path to the JWT private key")
    public_key: str = Field(..., description="Path to the JWT public key")
    algo: str = Field(
        default="RS256",
        description="JWT algorithm used for signing"
    )


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
    jwt: JwtConfig
    logger: logging.Logger = logging.getLogger("asterisk_api")


settings = Settings()  # Instantiate the settings object
