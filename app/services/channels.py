from dataclasses import dataclass
from typing import List

from app.schemas.responses.channel import Channel


@dataclass
class Channels:

    @staticmethod
    def map(items: list[dict]) -> List[Channel]:
        channel_info = []
        for item in items:
            if item.event == "CoreShowChannel":
                channel_info.append(Channel.model_validate(item))
        return channel_info
