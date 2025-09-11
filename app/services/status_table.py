from datetime import datetime
from zoneinfo import ZoneInfo
from panoramisk import Manager

from app.schemas.responses.queue_member import QueueMember, AgentState
from app.services.sip_peers import SipPeers, SipPeer
from app.services.channels import Channels, Channel
from app.schemas.responses.queue_entry import QueueEntry
from app.schemas.responses.hold import Hold
from app.schemas.responses.unhold import UnHold
from app.schemas.responses.queue_member_pause import QueueMemberPause
from app.schemas.responses.hangup import Hangup


class StatusTable:
    """
    A class that manages and tracks the status of queue members and calls in an Asterisk system.

    This class maintains a table of member statuses and queued calls, providing methods to:
    - Load and reload status data from the Asterisk Manager Interface (AMI)
    - Filter and count members by their various states
    - Track hold times and pause states
    - Monitor hangups and channel status
    - Generate status reports for specified queues
    """

    def __init__(self):
        self.__members_table: dict[str, QueueMember] = {}
        self.__queued_calls: list[QueueEntry] = []

    async def load_data(self, ami_manager: Manager):
        """
        Loads initial status data from the Asterisk Manager Interface (AMI).

        This method queries the AMI for queue status, SIP peers, and channel information,
        then populates the internal members table and queued calls list.

        Args:
            ami_manager (Manager): The Asterisk Manager Interface connection object

        The method performs the following:
        - Gets queue status information
        - Retrieves SIP peer details
        - Gets current channel information
        - Maps the data to internal data structures
        - Updates the members table and queued calls list
        """
        items = await ami_manager.send_action({'Action': 'QueueStatus'})
        peers = await ami_manager.send_action({'Action': 'SIPpeers'})
        channels = await ami_manager.send_action({'Action': 'CoreShowChannels'})
        channels = Channels.map(channels)
        channels = {channel.channel: channel for channel in channels}
        peers = SipPeers.map(peers)
        peers = {peer.objectname: peer for peer in peers}
        for item in items:
            if item.event == "QueueMember":
                member_model = QueueMember.model_validate(item)
                if member_model.status == AgentState.UNKNOWN.value:
                    continue
                member_model.campaigns = [member_model.campaign]
                member_model = self.__set_peers_and_channels(
                    member_model, peers, channels
                )
                if member_model.location not in self.__members_table:
                    self.__members_table[member_model.location] = member_model
                else:
                    self.__update_member(
                        member_model, peers, channels
                    )
            if item.event == "QueueEntry":
                call = QueueEntry.model_validate(item)
                self.__queued_calls.append(call)

    def count_by_state(self, data: list[dict]) -> dict[str, dict]:
        """
        Counts members by their current state and returns statistics for each state.

        Args:
            data (list[dict]): List of member dictionaries containing status information

        Returns:
            dict[str, dict]: Dictionary containing counts and metadata for each member state:
                - Keys are state names (e.g. 'BUSY', 'INUSE', etc.)
                - Values are dictionaries containing:
                    - count: Number of members in that state
                    - id: State identifier (for standard states)
                    - friendly_name: Human readable name for the state

        The method handles all standard member states (BUSY, INUSE, etc.) as well as
        special states like INPAUSE and ONLINE (total members online).
        """
        return {
            AgentState.AVAILABLE.name: {
                "count": len([
                    member for member in data if member["status"] == AgentState.AVAILABLE.value
                ]),
                "id": AgentState.AVAILABLE.value,
                "friendly_name": AgentState.AVAILABLE.friendly_name
            },
            AgentState.CALLING.name: {
                "count": len([
                    member for member in data if member["status"] == AgentState.CALLING.value
                ]),
                "id": AgentState.CALLING.value,
                "friendly_name": AgentState.CALLING.friendly_name
            },
            AgentState.DISCONNECTED.name: {
                "count": len([
                    member for member in data if member["status"] == AgentState.DISCONNECTED.value
                ]),
                "id": AgentState.DISCONNECTED.value,
                "friendly_name": AgentState.DISCONNECTED.friendly_name
            },
            AgentState.IN_PAUSE.name: {
                "count": len([
                    member for member in data if member["status"] == AgentState.IN_PAUSE.value
                ]),
                "id": AgentState.IN_PAUSE.value,
                "friendly_name": AgentState.IN_PAUSE.friendly_name
            },
            AgentState.ON_CALL.name: {
                "count": len([
                    member for member in data if member["status"] in [
                        AgentState.ON_CALL.value,
                        AgentState.ON_HOLD.value
                    ]
                ]),
                "id": AgentState.ON_CALL.value,
                "friendly_name": AgentState.ON_CALL.friendly_name
            },
            AgentState.ON_HOLD.name: {
                "count": len([
                    member for member in data if member["status"] == AgentState.ON_HOLD.value
                ]),
                "id": AgentState.ON_HOLD.value,
                "friendly_name": AgentState.ON_HOLD.friendly_name
            },
            "ONLINE": {
                "count": len([
                    member for member in data if member["status"] in [
                        AgentState.AVAILABLE.value,
                        AgentState.CALLING.value,
                        AgentState.ON_HOLD.value,
                        AgentState.ON_CALL.value,
                        AgentState.IN_PAUSE.value
                    ]
                ]),
                "friendly_name": "Total en linea."
            }
        }

    def filter(self, queue_names: list[str]) -> list[dict]:
        """
        Filters the members table by specified queue names.

        Args:
            queue_names (list[str]): List of queue names to filter by

        Returns:
            list[dict]: List of member dictionaries belonging to the specified queues,
                    with each member's data converted to a dictionary format
        """
        queue_names = [
            queue_name.replace("Q", "") for queue_name in queue_names
        ]
        queue_names = set(queue_names)
        return [
            member.model_dump() for member in self.__members_table.values() if len(
                list(set(member.campaigns) & queue_names)
            )
        ]

    async def reload(self, ami_manager: Manager):
        """
        Reloads and updates the status data from the Asterisk Manager Interface (AMI).

        This method refreshes the queue status, SIP peers, and channel information by
        querying the AMI. It updates existing member records and adds new ones as needed.

        Args:
            ami_manager (Manager): The Asterisk Manager Interface connection object

        The method performs the following:
        - Retrieves fresh queue status information
        - Gets updated SIP peer details
        - Gets current channel information
        - Updates existing member records while preserving state
        - Adds new members if they don't exist
        - Refreshes the queued calls list
        """
        items = await ami_manager.send_action({'Action': 'QueueStatus'})
        peers = await ami_manager.send_action({'Action': 'SIPpeers'})
        channels = await ami_manager.send_action({'Action': 'CoreShowChannels'})
        channels = Channels.map(channels)
        channels = {channel.channel: channel for channel in channels}
        peers = SipPeers.map(peers)
        peers = {peer.objectname: peer for peer in peers}
        items_exts = []
        self.__queued_calls = []
        for item in items:
            if item.event == "QueueMember":
                member_event = QueueMember.model_validate(item)
                if member_event.status == AgentState.UNKNOWN.value:
                    continue
                member_event.campaigns = [member_event.campaign]
                if member_event.location in self.__members_table:
                    self.__update_member(
                        member_event, peers, channels
                    )
                else:
                    member_event = self.__set_peers_and_channels(
                        member_event, peers, channels
                    )
                    self.__members_table[member_event.location] = member_event
                items_exts.append(member_event.location)
            if item.event == "QueueEntry":
                call = QueueEntry.model_validate(item)
                self.__queued_calls.append(call)
        self.set_disconnect_status(items_exts)

    def call_filter(self, queue_names: list[str]) -> list[dict]:
        """
        Filters queued calls by specified queue names.

        Args:
            queue_names (list[str]): List of queue names to filter by

        Returns:
            list[dict]: List of queued call dictionaries belonging to the specified queues,
                    with each call's data converted to a dictionary format
        """
        return [call.model_dump() for call in self.__queued_calls if call.queue in queue_names]

    def set_hold_time(self, event) -> None:
        """
        Sets the hold start time for a member based on a hold event.

        This method updates the hold_start_at timestamp for a member when they put a call on hold.
        It matches the channel from the hold event to find the correct member record to update.

        Args:
            event: The hold event containing channel and timestamp information

        The method:
        - Validates and converts the event to a Hold model
        - Finds the member with a matching channel/location
        - Updates their hold start timestamp
        - Updates the members table with the modified record
        """
        hold = Hold.model_validate(event)
        location = hold.channel
        for member in self.__members_table.values():
            if location == member.location:
                if member.phone_number != member.last_hold_phone_number:
                    member.hold_time_accumulator = "00:00:00"
                member.hold_start_at = hold.timestamp
                member.status = AgentState.ON_HOLD
                self.__members_table[location] = member

    def set_unhold(self, event) -> None:
        """
        Clears the hold time for a member based on an unhold event.

        This method removes the hold_start_at timestamp for a member when they take a call off hold.
        It matches the channel from the unhold event to find the correct member record to update.

        Args:
            event: The unhold event containing channel information

        The method:
        - Validates and converts the event to an UnHold model
        - Finds the member with a matching channel/location
        - Clears their hold start timestamp
        - Updates the members table with the modified record
        """
        unhold = UnHold.model_validate(event)
        location = unhold.channel
        for member in self.__members_table.values():
            if location == member.location:
                member.hold_time_accumulator = member.hold_time
                member.last_hold_phone_number = member.phone_number
                member.hold_start_at = None
                self.__members_table[location] = member

    def __set_peers_and_channels(
        self,
        model: QueueMember,
        peers: dict[str, SipPeer],
        channels: dict[str, Channel]
    ) -> QueueMember:
        """
        Sets the SIP peer and channel information for a member.

        This method updates a member record with SIP peer and channel details.
        It matches the member's location to find the corresponding peer and channel information.

        Args:
            model (MemberStatusTable): The member status data to update
            peers (dict[str, SipPeer]): Dictionary of SIP peers by name
            channels (dict[str, Channel]): Dictionary of channels by name

        Returns:
            MemberStatusTable: The updated member status data with peer and channel information
        """
        location = model.location
        if location in peers:
            model.ip_address = peers[location].ipaddress
            model.device_status = peers[location].status_name
        if location in channels:
            model.call_status = channels[location].channel_state_name
            model.duration = channels[location].duration
            model.phone_number = channels[location].conected_line_num
            model.channel_sip = channels[location].channel_sip
        return model

    def __update_member(
        self,
        model: QueueMember,
        peers: dict[str, SipPeer],
        channels: dict[str, Channel]
    ):
        """
        Updates an existing member record with fresh status data.

        This method:
        - Matches the member record using location/queue
        - Updates member status, name, IP address, and device status
        - Refreshes call status, duration, and phone number from channels
        - Preserves existing pause status and reason

        Args:
            model (MemberStatusTable): The member status data to update
            peers (dict[str, SipPeer]): Dictionary of SIP peers by name
            channels (dict[str, Channel]): Dictionary of channels by name

        The method:
        - Finds the member record using location/queue
        - Updates status, name, IP address, and device status
        - Refreshes call status, duration, and phone number from channels
        - Preserves existing pause status and reason
        - Updates the members table with the modified record
        """
        location = model.location
        member_table = self.__members_table[location]
        member_table.campaigns = list(
            set(member_table.campaigns + model.campaigns)
        )
        if model.paused != member_table.paused:
            member_table.paused = model.paused
            member_table.paused_reason = model.paused_reason
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
            member_table.channel_sip = channels[location].channel_sip
        else:
            member_table.call_status = "N/A"
            member_table.duration = "N/A"
            member_table.phone_number = "N/A"
            member_table.channel_sip = None
        member_table.validate_status()
        self.__members_table[location] = member_table

    def add_pause(self, event) -> None:
        """
        Updates a member's pause status based on a pause event.

        This method processes a queue member pause event and updates the corresponding
        member record with pause status, reason, and timestamp information.

        Args:
            event: The pause event containing member pause details including:
                - location: Member's channel/location
                - queue: Queue name
                - paused: Boolean pause status
                - paused_reason: Reason for the pause
                - timestamp: When the pause occurred

        The method:
        - Validates and converts the event to a QueueMemberPause model
        - Finds the member record using location/queue
        - Updates pause status, reason and timestamp
        - Updates the members table with modified record
        """
        pause = QueueMemberPause.model_validate(event)
        location = pause.location
        if location in self.__members_table:
            member = self.__members_table[location]
            member.paused = pause.paused
            member.paused_reason = pause.paused_reason
            member.paused_start_at = pause.timestamp
            self.__members_table[location] = member

    def listen_hangup(self, event) -> None:
        """
        Processes a hangup event and updates member status accordingly.

        This method handles hangup events by clearing the hold time for any member
        whose channel matches the hangup event's location.

        Args:
            event: The hangup event containing channel/location information

        The method:
        - Validates and converts the event to a Hangup model
        - Finds any member with a matching channel/location
        - Clears their hold start timestamp
        - Updates the members table with the modified record
        """
        hangup = Hangup.model_validate(event)
        location = hangup.location
        for member in self.__members_table.values():
            if location == member.location:
                member.hold_start_at = None
                member.hold_time_accumulator = "00:00:00"
                self.__members_table[location] = member

    def unique_values(self, data: list[dict]) -> list[dict]:
        """
        Filters a list of member dictionaries to return only unique members based on location.

        This method removes duplicate member entries by keeping only the latest entry
        for each unique location value.

        Args:
            data (list[dict]): List of member dictionaries containing status information

        Returns:
            list[dict]: List of unique member dictionaries, with duplicates removed based
                    on location field
        """
        uniques = {member["location"]: member for member in data}
        return list(uniques.values())

    def get_status(self, queues: list[str]) -> dict:
        """
        Gets the current status overview for specified queues.

        This method generates a comprehensive status report including:
        - Filtered and deduplicated member data
        - Total count of unique members
        - Member counts by state
        - Queued calls information
        - Total count of queued calls

        Args:
            queues (list[str]): List of queue names to get status for

        Returns:
            dict: Status report containing:
                - data_table: List of unique member records
                - total_rows: Count of unique members
                - counts: Member counts by state
                - queued_calls: List of queued call records
                - count_queued_calls: Count of queued calls
        """
        data_filtered = self.filter(queues)
        call_filtered = self.get_queued_calls(queues)
        campaigns_stats = self.set_queues_info_per_member()
        return {
            "data_table": data_filtered,
            "total_rows": len(data_filtered),
            "counts": self.count_by_state(data_filtered),
            "queued_calls": call_filtered["queued_calls"],
            "count_queued_calls": call_filtered["count_queued_calls"],
            "queues_stats" : list(campaigns_stats.values())
        }

    def get_queued_calls(self, queues: list[str]) -> dict:
        """
        Gets queued calls information for specified queues.

        This method filters the queued calls by queue names and returns both the
        filtered call list and total count.

        Args:
            queues (list[str]): List of queue names to filter calls by

        Returns:
            dict: Dictionary containing:
                - queued_calls: List of filtered call dictionaries
                - count_queued_calls: Total number of filtered calls
        """
        call_filtered = self.call_filter(queues)
        return {
            "queued_calls": call_filtered,
            "count_queued_calls": len(call_filtered)
        }

    def set_disconnect_status(self, connected_members: list) -> None:
        """
        Sets the disconnect status for all members in the members table.

        This method iterates through all members and sets their status to 'DISCONNECTED'.
        It is typically used when a member is no longer active or has been removed from the system.
        """
        for member in self.__members_table.values():
            if member.location in connected_members:
                if not member.is_connected:
                    member.is_connected = True
                    member.last_connection = "N/A"
                self.__members_table[member.location] = member
            else:
                if member.is_connected:
                    member.is_connected = False
                    member.status = AgentState.DISCONNECTED.value
                    member.last_connection = datetime.now(ZoneInfo("America/Bogota"))\
                        .strftime("%d/%b/%y %H:%M:%S")
                    member.paused = False
                    member.paused_reason = "N/A"
                    self.__members_table[member.location] = member

    def set_queues_info_per_member(self) -> dict[str, dict]:
        """
        Construye un dict con métricas por cola.
        """
        campaigns: dict[str, dict] = {}

        # contar llamadas en cola
        for call in self.__queued_calls:
            # Normalizamos el id de la queue (quita solo la Q inicial si la tiene)
            campaign_id = call.queue.lstrip("Q")
            if campaign_id not in campaigns:
                campaigns[campaign_id] = {
                    "id": campaign_id,
                    "queued_calls": 0,
                    "available_agents": 0
                }
            campaigns[campaign_id]["queued_calls"] += 1
    
        # contar agentes disponibles
        for member in self.__members_table.values():
            campaign_id = member.campaign  # ya devuelve sin "Q"
            if campaign_id not in campaigns:
                campaigns[campaign_id] = {
                    "id": campaign_id,
                    "queued_calls": 0,
                    "available_agents": 0
                }
            if member.status == AgentState.AVAILABLE.value:
                campaigns[campaign_id]["available_agents"] += 1

        return campaigns