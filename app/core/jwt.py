from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from dotenv import load_dotenv
from jwt import decode, PyJWTError
from jwt.exceptions import InvalidTokenError

from app.core.config import settings
from app.exceptions.jwt_exceptions import (
    JwtFileNotFoundException,
    JwtInvalidTokenException,
    JwtPyJWTErrorException
)

jwt = settings.jwt


def verify_token(token: str):
    """Verifica si el token es valido y retorna la data descifrada"""
    try:
        payload = None
        load_dotenv()
        with open(jwt.public_key, "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )
        payload = decode(token, public_key, algorithms=[jwt.algo])
    except InvalidTokenError:
        raise JwtInvalidTokenException
    except PyJWTError:
        raise JwtPyJWTErrorException
    except FileNotFoundError:
        raise JwtFileNotFoundException

    return payload
