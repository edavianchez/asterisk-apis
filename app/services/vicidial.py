import asyncio
import re
from panoramisk import Manager
from panoramisk.message import Message
from typing import List, Dict, Any, Optional


class VicidialService:
    OPERATION_QUEUES = {
        1: [83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 105],
        2: [127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142,
            143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158,
            159, 160, 161, 162, 163, 164, 165, 166],
    }

    async def execute_command(self, manager: Manager, campaign: Optional[int] = None, operation: Optional[int] = None) -> Dict[str, Any]:
        queues_to_query = []
        if campaign:
            queues_to_query = [campaign]
        elif operation and operation in self.OPERATION_QUEUES:
            queues_to_query = self.OPERATION_QUEUES[operation]
        else:
            return {"error": "Invalid campaign or operation specified."}

        queue_status_tasks = [
            manager.send_action(
                {'Action': 'QueueStatus', 'Queue': f'q{q}'})  # ✅
            for q in queues_to_query
        ]

        all_queues_task = manager.send_action({'Action': 'QueueStatus'})  # ✅
        sip_peers_task = manager.send_action({'Action': 'SIPpeers'})  # ✅
        core_channels_task = manager.send_action(
            {'Action': 'CoreShowChannels'})

        tasks = queue_status_tasks + \
            [all_queues_task, sip_peers_task, core_channels_task]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        queue_status_results = results[:len(queue_status_tasks)]
        all_queues_result = results[len(queue_status_tasks)]
        sip_peers_result = results[len(queue_status_tasks) + 1]
        core_channels_result = results[len(queue_status_tasks) + 2]

        combined_queue_status = [item for sublist in queue_status_results if isinstance(
            sublist, list) for item in sublist]

        agent_details = self._get_agent_details(
            combined_queue_status, sip_peers_result, core_channels_result)
        calls_in_queue = self._extract_calls_in_queue(combined_queue_status)
        members_summary_all = self._extract_queue_all(all_queues_result)

        return {
            'agentDetails': agent_details,
            'callsInQueue': calls_in_queue,
            'membersSummaryAll': members_summary_all,
            'campaign': f"Campaign {campaign}" if campaign else f"Operation {operation}"
        }

    def _get_agent_details(self, queue_messages: List[Message], peer_messages: List[Message], channel_messages: List[Message]) -> List[Dict[str, Any]]:
        agents = {}

        if isinstance(queue_messages, list):
            for msg in queue_messages:
                if msg.event == 'QueueMember':
                    name = msg.get('Name')
                    if name and 'SIP/' in name:
                        exten = name.split('/')[1]
                        if exten not in agents:
                            agents[exten] = {}
                        agents[exten]['extension'] = exten
                        agents[exten]['state'] = msg.get('Status')
                        agents[exten]['paused'] = bool(
                            int(msg.get('Paused', 0)))
                        agents[exten]['name'] = msg.get('MemberName')

        if isinstance(peer_messages, list):
            for msg in peer_messages:
                if msg.event == 'PeerEntry':
                    exten = msg.get('ObjectName')
                    if exten in agents:
                        agents[exten]['ipUser'] = msg.get('Address')

        if isinstance(channel_messages, list):
            for msg in channel_messages:
                if msg.event == 'CoreShowChannel':
                    channel_name = msg.get('Channel')
                    if channel_name:
                        match = re.match(r"SIP/(\d+)-", channel_name)
                        if match:
                            exten = match.group(1)
                            if exten in agents:
                                agents[exten]['duration'] = msg.get('Duration')
                                agents[exten]['connected_number'] = msg.get(
                                    'ConnectedLineNum')

        return list(agents.values())

    def _extract_calls_in_queue(self, queue_messages: List[Message]) -> List[Dict[str, Any]]:
        callers = []
        if not isinstance(queue_messages, list):
            return callers
        for msg in queue_messages:
            if msg.event == 'QueueEntry':
                callers.append({
                    "queue": msg.get('Queue'),
                    "position": msg.get('Position'),
                    "channel": msg.get('Channel'),
                    "caller_id": msg.get('CallerIDNum'),
                    "wait_time": msg.get('Wait')
                })
        return callers

    def _extract_queue_all(self, all_queues_messages: List[Message]) -> List[Dict[str, Any]]:
        queues = {}
        if not isinstance(all_queues_messages, list):
            return list(queues.values())
        for msg in all_queues_messages:
            if msg.event == 'QueueParams':
                queue_name = msg.get('Queue')
                if queue_name not in queues:
                    queues[queue_name] = {'name': queue_name, 'calls': 0}
                queues[queue_name]['calls'] = int(msg.get('Calls', 0))
        return list(queues.values())
