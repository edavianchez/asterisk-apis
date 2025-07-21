from panoramisk import Manager

from app.schemas.responses.member_status_table import MemberStatusTable
from app.schemas.responses.queue_member import MemberState
from app.services.sip_peers import SipPeers
from app.services.channels import Channels
from app.schemas.responses.queue_entry import QueueEntry


class StatusTable:
    def __init__(self):
        self.__table: dict[str, MemberStatusTable] = {}
        self.__queued_calls: dict[str, QueueEntry] = {}

    async def load_data(self, ami_manager: Manager):
        members = await ami_manager.send_action({'Action': 'QueueStatus'})
        peers = await ami_manager.send_action({'Action': 'SIPpeers'})
        channels = await ami_manager.send_action({'Action': 'CoreShowChannels'})
        channels = Channels.map(channels)
        channels = {channel.channel.split(
            "-")[0].replace("SIP/", ""): channel for channel in channels}
        peers = SipPeers.map(peers)
        peers = {peer.objectname: peer for peer in peers}
        for member in members:
            if member.event == "QueueMember":
                location = member.location.replace("SIP/", "")
                member_model = MemberStatusTable.model_validate(member)
                if location in peers:
                    member_model.ip_address = peers[location].ipaddress
                    member_model.device_status = peers[location].status_name
                if location in channels:
                    member_model.call_status = channels[location].channel_state_name
                    member_model.duration = channels[location].duration
                    member_model.phone_number = channels[location].conected_line_num
                self.__table[location] = member_model.model_dump()
            if member.event == "QueueEntry":
                call = QueueEntry.model_validate(member)
                self.__queued_calls[call.channel] = call.model_dump()

    def count_by_state(self, data: dict[str, MemberStatusTable]):
        return {
            MemberState.BUSY.name: {
                "count": len([
                    member for member in data if member["status"] == MemberState.BUSY.value
                ]),
                "id": MemberState.BUSY.value,
                "friendly_name": MemberState.BUSY.friendly_name
            },
            MemberState.INUSE.name: {
                "count": len([
                    member for member in data if member["status"] == MemberState.INUSE.value
                ]),
                "id": MemberState.INUSE.value,
                "friendly_name": MemberState.INUSE.friendly_name
            },
            MemberState.INVALID.name: {
                "count": len([
                    member for member in data if member["status"] == MemberState.INVALID.value
                ]),
                "id": MemberState.INVALID.value,
                "friendly_name": MemberState.INVALID.friendly_name
            },
            MemberState.NOT_INUSE.name: {
                "count": len([
                    member for member in data if member["status"] == MemberState.NOT_INUSE.value
                ]),
                "id": MemberState.NOT_INUSE.value,
                "friendly_name": MemberState.NOT_INUSE.friendly_name
            },
            MemberState.ONHOLD.name: {
                "count": len([
                    member for member in data if member["status"] == MemberState.ONHOLD.value
                ]),
                "id": MemberState.ONHOLD.value,
                "friendly_name": MemberState.ONHOLD.friendly_name
            },
            MemberState.RINGING.name: {
                "count": len([
                    member for member in data if member["status"] == MemberState.RINGING.value
                ]),
                "id": MemberState.RINGING.value,
                "friendly_name": MemberState.RINGING.friendly_name
            },
            MemberState.RINGINUSE.name: {
                "count": len([
                    member for member in data if member["status"] == MemberState.RINGINUSE.value
                ]),
                "id": MemberState.RINGINUSE.value,
                "friendly_name": MemberState.RINGINUSE.friendly_name
            },
            MemberState.UNAVAILABLE.name: {
                "count": len([
                    member for member in data if member["status"] == MemberState.UNAVAILABLE.value
                ]),
                "id": MemberState.UNAVAILABLE.value,
                "friendly_name": MemberState.UNAVAILABLE.friendly_name
            },
            MemberState.UNKNOWN.name: {
                "count": len([
                    member for member in data if member["status"] == MemberState.UNKNOWN.value
                ]),
                "id": MemberState.UNKNOWN.value,
                "friendly_name": MemberState.UNKNOWN.friendly_name
            },
            MemberState.INPAUSE.name: {
                "count": len([member for member in data if member["paused"]]),
                "friendly_name": "En pausa"
            },
            "ONLINE": {
                "count": len([
                    member for member in data if member["status"] in [
                        MemberState.NOT_INUSE.value,
                        MemberState.BUSY.value,
                        MemberState.RINGING.value,
                        MemberState.RINGINUSE.value,
                        MemberState.ONHOLD.value,
                    ]
                ]),
                "friendly_name": "Total en linea."
            }
        }

    def filter(self, queue_names: list[str]) -> list[dict]:
        return [member for _, member in self.__table.items() if member["queue"] in queue_names]

    async def reload(self, ami_manager: Manager):
        members = await ami_manager.send_action({'Action': 'QueueStatus'})
        peers = await ami_manager.send_action({'Action': 'SIPpeers'})
        channels = await ami_manager.send_action({'Action': 'CoreShowChannels'})
        channels = Channels.map(channels)
        channels = {channel.channel.split(
            "-")[0].replace("SIP/", ""): channel for channel in channels}
        peers = SipPeers.map(peers)
        peers = {peer.objectname: peer for peer in peers}
        for member in members:
            if member.event == "QueueMember":
                location = member.location.replace("SIP/", "")
                member_model = MemberStatusTable.model_validate(member)
                if location in peers:
                    member_model.ip_address = peers[location].ipaddress
                    member_model.device_status = peers[location].status_name
                else:
                    member_model.ip_address = "N/A"
                    member_model.device_status = "N/A"
                if location in channels:
                    member_model.call_status = channels[location].channel_state_name
                    member_model.duration = channels[location].duration
                    member_model.phone_number = channels[location].conected_line_num
                else:
                    member_model.call_status = "N/A"
                    member_model.duration = "N/A"
                    member_model.phone_number = "N/A"
                self.__table[location] = member_model.model_dump()
            if member.event == "QueueEntry":
                call = QueueEntry.model_validate(member)
                self.__queued_calls[call.channel] = call.model_dump()

    def call_filter(self, queue_names: list[str]) -> list[dict]:
        return [call for _, call in self.__queued_calls.items() if call["queue"] in queue_names]
