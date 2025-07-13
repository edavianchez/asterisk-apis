from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from jwt import decode, encode, PyJWTError
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
        with open(jwt.public_key, "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )
        payload = decode(token, public_key, algorithms=[jwt.algo])
    except InvalidTokenError as e:
        settings.logger.error(f"Invalid token: {e}")
        raise JwtInvalidTokenException
    except PyJWTError:
        raise JwtPyJWTErrorException
    except FileNotFoundError:
        raise JwtFileNotFoundException

    return payload


def create_jwt(to_encode: dict[str, str]) -> str:
    with open(jwt.private_key, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            backend=default_backend(),
            password=None  # Assuming the private key is not encrypted
        )
    encoded_jwt = encode(
        to_encode, private_key, algorithm=jwt.algo
    )
    return encoded_jwt
