from dataclasses import dataclass
from panoramisk.message import Message

from app.schemas.responses.queue import Queue, QueueWithMembers
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
    def map_details(items: list[Message], queue_name: str) -> Queue | None:
        """
        Get details of a specific queue.
        """
        for item in items:
            if item.event == 'QueueParams' and item.queue == queue_name:
                return Queue.model_validate(item)
        return None

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

    @staticmethod
    def map_with_members(items: list[Message], queue_names: list[str]) -> list[QueueWithMembers]:
        """
        Get details of a specific queue with its members.
        """
        queue_info = []
        for item in items:
            if item.event == 'QueueParams' and item.queue in queue_names:
                queue_info.append(QueueWithMembers.model_validate(item))
            elif item.event == 'QueueMember' and item.queue in queue_names:
                member = QueueMember.model_validate(item)
                for queue in queue_info:
                    if queue.queue == item.queue:
                        queue.members.append(member)
        return queue_info
