from panoramisk import Manager

from app.schemas.responses.member_status_table import MemberStatusTable
from app.schemas.responses.queue_member import MemberState
from app.services.sip_peers import SipPeers, SipPeer
from app.services.channels import Channels, Channel
from app.schemas.responses.queue_entry import QueueEntry
from app.schemas.responses.hold import Hold
from app.schemas.responses.unhold import UnHold
from app.schemas.responses.queue_member_pause import QueueMemberPause
from app.schemas.responses.hangup import Hangup


class StatusTable:
    def __init__(self):
        self.__members_table: dict[str, MemberStatusTable] = {}
        self.__queued_calls: list[QueueEntry] = []

    async def load_data(self, ami_manager: Manager):
        items = await ami_manager.send_action({'Action': 'QueueStatus'})
        peers = await ami_manager.send_action({'Action': 'SIPpeers'})
        channels = await ami_manager.send_action({'Action': 'CoreShowChannels'})
        channels = Channels.map(channels)
        channels = {channel.channel.split(
            "-")[0].replace("SIP/", "ext. "): channel for channel in channels}
        peers = SipPeers.map(peers)
        peers = {f"ext. {peer.objectname}": peer for peer in peers}
        for item in items:
            if item.event == "QueueMember":
                member_model = MemberStatusTable.model_validate(item)
                member_model = self.__set_peers_and_channels(
                    member_model, peers, channels
                )
                self.__members_table[member_model.location] = member_model
            if item.event == "QueueEntry":
                call = QueueEntry.model_validate(item)
                self.__queued_calls.append(call)

    def count_by_state(self, data: list[dict]) -> dict[str, dict]:
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
            "INPAUSE": {
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
                        MemberState.INUSE.value
                    ]
                ]) + len([member for member in data if member["paused"]]),
                "friendly_name": "Total en linea."
            }
        }

    def filter(self, queue_names: list[str]) -> list[dict]:
        return [member.model_dump() for member in self.__members_table.values() if member.queue in queue_names]

    async def reload(self, ami_manager: Manager):
        self.__queued_calls = []
        items = await ami_manager.send_action({'Action': 'QueueStatus'})
        peers = await ami_manager.send_action({'Action': 'SIPpeers'})
        channels = await ami_manager.send_action({'Action': 'CoreShowChannels'})
        channels = Channels.map(channels)
        channels = {channel.channel.split(
            "-")[0].replace("SIP/", ""): channel for channel in channels}
        peers = SipPeers.map(peers)
        peers = {peer.objectname: peer for peer in peers}
        for item in items:
            if item.event == "QueueMember":
                member_event = MemberStatusTable.model_validate(item)
                location = member_event.location
                if location in self.__members_table:
                    self.__update_member(
                        member_event, peers, channels
                    )
                else:
                    member_event = self.__set_peers_and_channels(
                        member_event, peers, channels
                    )
                    self.__members_table[location] = member_event
            if item.event == "QueueEntry":
                call = QueueEntry.model_validate(item)
                self.__queued_calls.append(call)

    def call_filter(self, queue_names: list[str]) -> list[dict]:
        return [call.model_dump() for call in self.__queued_calls if call.queue in queue_names]

    def set_hold_time(self, event):
        hold = Hold.model_validate(event)
        location = hold.channel
        if location in self.__members_table:
            member = self.__members_table[location]
            member.hold_start_at = hold.timestamp
            self.__members_table[location] = member

    def set_unhold(self, event):
        unhold = UnHold.model_validate(event)
        location = unhold.channel
        if location in self.__members_table:
            member = self.__members_table[location]
            member.hold_start_at = None
            self.__members_table[location] = member

    def __set_peers_and_channels(
        self,
        model: MemberStatusTable,
        peers: dict[str, SipPeer],
        channels: dict[str, Channel]
    ) -> MemberStatusTable:
        location = model.location
        if location in peers:
            model.ip_address = peers[location].ipaddress
            model.device_status = peers[location].status_name
        if location in channels:
            model.call_status = channels[location].channel_state_name
            model.duration = channels[location].duration
            model.phone_number = channels[location].conected_line_num
        return model

    def __update_member(
        self,
        model: MemberStatusTable,
        peers: dict[str, SipPeer],
        channels: dict[str, Channel]
    ):
        location = model.location
        member_table = self.__members_table[location]
        member_table.name = model.name
        member_table.status = model.status
        if location in peers:
            member_table.ip_address = peers[location].ipaddress
            member_table.device_status = peers[location].status_name
        else:
            member_table.ip_address = "N/A"
            member_table.device_status = "N/A"
        if location in channels:
            member_table.call_status = channels[location].channel_state_name
            member_table.duration = channels[location].duration
            member_table.phone_number = channels[location].conected_line_num
        else:
            member_table.call_status = "N/A"
            member_table.duration = "N/A"
            member_table.phone_number = "N/A"
        self.__members_table[location] = member_table

    def add_pause(self, event):
        pause = QueueMemberPause.model_validate(event)
        location = pause.location
        if location in self.__members_table:
            member = self.__members_table[location]
            member.paused = pause.paused
            member.paused_reason = pause.paused_reason
            member.paused_start_at = pause.timestamp
            self.__members_table[location] = member

    def listen_hangup(self, event):
        hangup = Hangup.model_validate(event)
        location = hangup.location
        if location in self.__members_table:
            member = self.__members_table[location]
            member.hold_start_at = None
            self.__members_table[location] = member
