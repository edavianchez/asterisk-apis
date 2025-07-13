from datetime import datetime, timedelta
from typing import List
from xml.etree import ElementTree as ET
from panoramisk.message import Message

from app.core.config import settings
from app.core.jwt import create_jwt

jwt_config = settings.jwt


def list_messages(messages: List[str]) -> List[Message]:
    for idx, message in enumerate(messages):
        message += "</Message>"
        message_elem = ET.fromstring(message)
        message_dict = message_elem.attrib
        message_body = message_dict.pop('content', None)
        messages[idx] = Message(message_dict, message_body)
    return messages


def create_test_jwt() -> str:
    expire = datetime.now() + timedelta(minutes=30)
    to_encode = {
        "sub": "20",
        "username": "jwt_normal_user",
        "is_admin": "True",
        "exp": expire.timestamp()
    }
    return create_jwt(to_encode)
