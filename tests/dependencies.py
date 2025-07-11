from typing import List
from xml.etree import ElementTree as ET
from panoramisk.message import Message


def list_messages(messages: List[str]) -> List[Message]:
    for idx, message in enumerate(messages):
        message += "</Message>"
        message_elem = ET.fromstring(message)
        message_dict = message_elem.attrib
        message_body = message_dict.pop('content', None)
        messages[idx] = Message(message_dict, message_body)
    return messages
