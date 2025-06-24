from dataclasses import dataclass
from panoramisk.message import Message

from app.schemas.responses.queue import Queue
from app.schemas.responses.queue_member import QueueMember


@dataclass
class Queues:

    @staticmethod
    def map(items: list[Message]) -> list[Queue]:
        """
        List all queues.
        """
        queues_info = []
        # 'QueueStatus' genera múltiples eventos, por lo que iteramos
        for item in items:
            if item.event == 'QueueParams':
                # Este evento contiene los parámetros generales de la cola
                queues_info.append(Queue.model_validate(item))
        return queues_info

    @staticmethod
    def map_members(items: list[Message], queue_name: str) -> list[QueueMember]:
        """
        List all members of a specific queue.
        """
        members_info = []
        for item in items:
            if item.event == 'QueueMember' and item.queue == queue_name:
                members_info.append(QueueMember.model_validate(item))
        return members_info
