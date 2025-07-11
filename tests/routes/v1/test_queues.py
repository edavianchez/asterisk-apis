import unittest

from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from fastapi import status
from main import app
from app.dependencies import get_ami_manager
from app.core.config import settings
from tests.dependencies import list_messages


class QueuesApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app, base_url=settings.app_url)
        self.mock = MagicMock()
        self.mock.send_action = AsyncMock()

    def tearDown(self):
        app.dependency_overrides = {}

    def test_list_queues_success(self):
        # Mock the dependency
        app.dependency_overrides[get_ami_manager] = lambda: self.mock

        # Mock the AMI response
        messages = [
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' EventList='start' Message='Queue status will follow' Response='Success' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q32' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2027' LoginTime='1751577428' Membership='dynamic' Name='santiago.molina' Paused='0' PausedReason='' Penalty='0' Queue='Q32' StateInterface='SIP/2027' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2028' LoginTime='1751555966' Membership='dynamic' Name='luis.burgos' Paused='0' PausedReason='' Penalty='0' Queue='Q32' StateInterface='SIP/2028' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2021' LoginTime='1751905590' Membership='dynamic' Name='rafael.avila' Paused='0' PausedReason='' Penalty='0' Queue='Q32' StateInterface='SIP/2021' Status='5' Wrapuptime='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q31' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2027' LoginTime='1751577428' Membership='dynamic' Name='santiago.molina' Paused='0' PausedReason='' Penalty='0' Queue='Q31' StateInterface='SIP/2027' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2028' LoginTime='1751555966' Membership='dynamic' Name='luis.burgos' Paused='0' PausedReason='' Penalty='0' Queue='Q31' StateInterface='SIP/2028' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2021' LoginTime='1751905590' Membership='dynamic' Name='rafael.avila' Paused='0' PausedReason='' Penalty='0' Queue='Q31' StateInterface='SIP/2021' Status='5' Wrapuptime='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q8' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2017' LoginTime='1751563002' Membership='dynamic' Name='luis.burgos' Paused='0' PausedReason='' Penalty='0' Queue='Q8' StateInterface='SIP/2017' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2014' LoginTime='1752079488' Membership='dynamic' Name='natalia.merchan' Paused='0' PausedReason='' Penalty='0' Queue='Q8' StateInterface='SIP/2014' Status='5' Wrapuptime='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q30' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2027' LoginTime='1751577428' Membership='dynamic' Name='santiago.molina' Paused='0' PausedReason='' Penalty='0' Queue='Q30' StateInterface='SIP/2027' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2028' LoginTime='1751555966' Membership='dynamic' Name='luis.burgos' Paused='0' PausedReason='' Penalty='0' Queue='Q30' StateInterface='SIP/2028' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2021' LoginTime='1751905590' Membership='dynamic' Name='rafael.avila' Paused='0' PausedReason='' Penalty='0' Queue='Q30' StateInterface='SIP/2021' Status='5' Wrapuptime='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q9' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2017' LoginTime='1751563002' Membership='dynamic' Name='luis.burgos' Paused='0' PausedReason='' Penalty='0' Queue='Q9' StateInterface='SIP/2017' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2014' LoginTime='1752079488' Membership='dynamic' Name='natalia.merchan' Paused='0' PausedReason='' Penalty='0' Queue='Q9' StateInterface='SIP/2014' Status='5' Wrapuptime='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q26' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q27' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2027' LoginTime='1751577428' Membership='dynamic' Name='santiago.molina' Paused='0' PausedReason='' Penalty='0' Queue='Q27' StateInterface='SIP/2027' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2028' LoginTime='1751555966' Membership='dynamic' Name='luis.burgos' Paused='0' PausedReason='' Penalty='0' Queue='Q27' StateInterface='SIP/2028' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2021' LoginTime='1751905590' Membership='dynamic' Name='rafael.avila' Paused='0' PausedReason='' Penalty='0' Queue='Q27' StateInterface='SIP/2021' Status='5' Wrapuptime='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q24' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q25' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q22' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q39' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q23' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q38' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q20' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2002' LoginTime='1751920890' Membership='dynamic' Name='natalia.merchan' Paused='0' PausedReason='' Penalty='0' Queue='Q20' StateInterface='SIP/2002' Status='5' Wrapuptime='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q21' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='outbound' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q28' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2027' LoginTime='1751577428' Membership='dynamic' Name='santiago.molina' Paused='0' PausedReason='' Penalty='0' Queue='Q28' StateInterface='SIP/2027' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2028' LoginTime='1751555966' Membership='dynamic' Name='luis.burgos' Paused='0' PausedReason='' Penalty='0' Queue='Q28' StateInterface='SIP/2028' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2021' LoginTime='1751905590' Membership='dynamic' Name='rafael.avila' Paused='0' PausedReason='' Penalty='0' Queue='Q28' StateInterface='SIP/2021' Status='5' Wrapuptime='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q29' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2027' LoginTime='1751577428' Membership='dynamic' Name='santiago.molina' Paused='0' PausedReason='' Penalty='0' Queue='Q29' StateInterface='SIP/2027' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2028' LoginTime='1751555966' Membership='dynamic' Name='luis.burgos' Paused='0' PausedReason='' Penalty='0' Queue='Q29' StateInterface='SIP/2028' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2021' LoginTime='1751905590' Membership='dynamic' Name='rafael.avila' Paused='0' PausedReason='' Penalty='0' Queue='Q29' StateInterface='SIP/2021' Status='5' Wrapuptime='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q57' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q56' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='ventas' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q40' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='soporte' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='testQa' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q15' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2017' LoginTime='1751563002' Membership='dynamic' Name='luis.burgos' Paused='0' PausedReason='' Penalty='0' Queue='Q15' StateInterface='SIP/2017' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2014' LoginTime='1752079488' Membership='dynamic' Name='natalia.merchan' Paused='0' PausedReason='' Penalty='0' Queue='Q15' StateInterface='SIP/2014' Status='5' Wrapuptime='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q14' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2017' LoginTime='1751563002' Membership='dynamic' Name='luis.burgos' Paused='0' PausedReason='' Penalty='0' Queue='Q14' StateInterface='SIP/2017' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2014' LoginTime='1752079488' Membership='dynamic' Name='natalia.merchan' Paused='0' PausedReason='' Penalty='0' Queue='Q14' StateInterface='SIP/2014' Status='5' Wrapuptime='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q17' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2002' LoginTime='1751920890' Membership='dynamic' Name='natalia.merchan' Paused='0' PausedReason='' Penalty='0' Queue='Q17' StateInterface='SIP/2002' Status='5' Wrapuptime='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q16' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2151' LoginTime='1751555966' Membership='dynamic' Name='dmunoz40' Paused='0' PausedReason='' Penalty='0' Queue='Q16' StateInterface='SIP/2151' Status='4' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2017' LoginTime='1751563002' Membership='dynamic' Name='luis.burgos' Paused='0' PausedReason='' Penalty='0' Queue='Q16' StateInterface='SIP/2017' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2014' LoginTime='1752079488' Membership='dynamic' Name='natalia.merchan' Paused='0' PausedReason='' Penalty='0' Queue='Q16' StateInterface='SIP/2014' Status='5' Wrapuptime='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q11' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q90' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q10' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message Abandoned='9' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='52' Event='QueueParams' Holdtime='21' Max='100' Queue='Q88' ServiceLevel='0' ServicelevelPerf='46.2' ServicelevelPerf2='41.0' Strategy='leastrecent' TalkTime='63' Weight='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q4' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2017' LoginTime='1751563002' Membership='dynamic' Name='luis.burgos' Paused='0' PausedReason='' Penalty='0' Queue='Q4' StateInterface='SIP/2017' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2014' LoginTime='1752079488' Membership='dynamic' Name='natalia.merchan' Paused='0' PausedReason='' Penalty='0' Queue='Q4' StateInterface='SIP/2014' Status='5' Wrapuptime='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q13' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2017' LoginTime='1751563002' Membership='dynamic' Name='luis.burgos' Paused='0' PausedReason='' Penalty='0' Queue='Q13' StateInterface='SIP/2017' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2014' LoginTime='1752079488' Membership='dynamic' Name='natalia.merchan' Paused='0' PausedReason='' Penalty='0' Queue='Q13' StateInterface='SIP/2014' Status='5' Wrapuptime='0' content=''>",
            "<Message Abandoned='14' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='26' Event='QueueParams' Holdtime='3' Max='100' Queue='Q5' ServiceLevel='0' ServicelevelPerf='42.3' ServicelevelPerf2='27.5' Strategy='leastrecent' TalkTime='86' Weight='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2034' LoginTime='1751555966' Membership='dynamic' Name='natalia.merchan' Paused='0' PausedReason='' Penalty='0' Queue='Q5' StateInterface='SIP/2034' Status='5' Wrapuptime='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q12' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2017' LoginTime='1751563002' Membership='dynamic' Name='luis.burgos' Paused='0' PausedReason='' Penalty='0' Queue='Q12' StateInterface='SIP/2017' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2014' LoginTime='1752079488' Membership='dynamic' Name='natalia.merchan' Paused='0' PausedReason='' Penalty='0' Queue='Q12' StateInterface='SIP/2014' Status='5' Wrapuptime='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q6' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2017' LoginTime='1751563002' Membership='dynamic' Name='luis.burgos' Paused='0' PausedReason='' Penalty='0' Queue='Q6' StateInterface='SIP/2017' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2014' LoginTime='1752079488' Membership='dynamic' Name='natalia.merchan' Paused='0' PausedReason='' Penalty='0' Queue='Q6' StateInterface='SIP/2014' Status='5' Wrapuptime='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q7' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2017' LoginTime='1751563002' Membership='dynamic' Name='luis.burgos' Paused='0' PausedReason='' Penalty='0' Queue='Q7' StateInterface='SIP/2017' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2014' LoginTime='1752079488' Membership='dynamic' Name='natalia.merchan' Paused='0' PausedReason='' Penalty='0' Queue='Q7' StateInterface='SIP/2014' Status='5' Wrapuptime='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q84' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q85' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message Abandoned='7' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='66' Event='QueueParams' Holdtime='8' Max='1000' Queue='Q1' ServiceLevel='0' ServicelevelPerf='34.8' ServicelevelPerf2='31.5' Strategy='leastrecent' TalkTime='52' Weight='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2002' LoginTime='1751920890' Membership='dynamic' Name='natalia.merchan' Paused='0' PausedReason='' Penalty='0' Queue='Q1' StateInterface='SIP/2002' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2151' LoginTime='1751555966' Membership='dynamic' Name='dmunoz40' Paused='0' PausedReason='' Penalty='0' Queue='Q1' StateInterface='SIP/2151' Status='4' Wrapuptime='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q37' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q86' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message Abandoned='18' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q2' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='rrmemory' TalkTime='0' Weight='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q19' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2002' LoginTime='1751920890' Membership='dynamic' Name='natalia.merchan' Paused='0' PausedReason='' Penalty='0' Queue='Q19' StateInterface='SIP/2002' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2151' LoginTime='1751555966' Membership='dynamic' Name='dmunoz40' Paused='0' PausedReason='' Penalty='0' Queue='Q19' StateInterface='SIP/2151' Status='4' Wrapuptime='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='1000' Queue='Q36' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q87' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message Abandoned='14' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='44' Event='QueueParams' Holdtime='0' Max='20000' Queue='Q3' ServiceLevel='0' ServicelevelPerf='45.5' ServicelevelPerf2='34.5' Strategy='leastrecent' TalkTime='93' Weight='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2027' LoginTime='1751577428' Membership='dynamic' Name='santiago.molina' Paused='0' PausedReason='' Penalty='0' Queue='Q3' StateInterface='SIP/2027' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2028' LoginTime='1751555966' Membership='dynamic' Name='luis.burgos' Paused='0' PausedReason='' Penalty='0' Queue='Q3' StateInterface='SIP/2028' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2021' LoginTime='1751905590' Membership='dynamic' Name='rafael.avila' Paused='0' PausedReason='' Penalty='0' Queue='Q3' StateInterface='SIP/2021' Status='5' Wrapuptime='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q18' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2002' LoginTime='1751920890' Membership='dynamic' Name='natalia.merchan' Paused='0' PausedReason='' Penalty='0' Queue='Q18' StateInterface='SIP/2002' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2151' LoginTime='1751555966' Membership='dynamic' Name='dmunoz40' Paused='0' PausedReason='' Penalty='0' Queue='Q18' StateInterface='SIP/2151' Status='4' Wrapuptime='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q35' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2027' LoginTime='1751577428' Membership='dynamic' Name='santiago.molina' Paused='0' PausedReason='' Penalty='0' Queue='Q35' StateInterface='SIP/2027' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2028' LoginTime='1751555966' Membership='dynamic' Name='luis.burgos' Paused='0' PausedReason='' Penalty='0' Queue='Q35' StateInterface='SIP/2028' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2021' LoginTime='1751905590' Membership='dynamic' Name='rafael.avila' Paused='0' PausedReason='' Penalty='0' Queue='Q35' StateInterface='SIP/2021' Status='5' Wrapuptime='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q80' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q34' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2027' LoginTime='1751577428' Membership='dynamic' Name='santiago.molina' Paused='0' PausedReason='' Penalty='0' Queue='Q34' StateInterface='SIP/2027' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2028' LoginTime='1751555966' Membership='dynamic' Name='luis.burgos' Paused='0' PausedReason='' Penalty='0' Queue='Q34' StateInterface='SIP/2028' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2021' LoginTime='1751905590' Membership='dynamic' Name='rafael.avila' Paused='0' PausedReason='' Penalty='0' Queue='Q34' StateInterface='SIP/2021' Status='5' Wrapuptime='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q81' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message Abandoned='0' ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q33' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2027' LoginTime='1751577428' Membership='dynamic' Name='santiago.molina' Paused='0' PausedReason='' Penalty='0' Queue='Q33' StateInterface='SIP/2027' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2028' LoginTime='1751555966' Membership='dynamic' Name='luis.burgos' Paused='0' PausedReason='' Penalty='0' Queue='Q33' StateInterface='SIP/2028' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2021' LoginTime='1751905590' Membership='dynamic' Name='rafael.avila' Paused='0' PausedReason='' Penalty='0' Queue='Q33' StateInterface='SIP/2021' Status='5' Wrapuptime='0' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Event='QueueStatusComplete' EventList='Complete' ListItems='114' content=''>"
        ]
        self.mock.send_action.return_value = list_messages(messages)

        response = self.client.get("/api/v1/queues/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            "Response status code should be 200 OK"
        )
        data = response.json()
        self.assertDictEqual(
            data[34],
            {
                "queue": "Q5",
                "strategy": "leastrecent",
                "calls": "0",
                "holdtime": "3",
                "talktime": "86",
                "completed": "26",
                "abandoned": "14",
                "servicelevel": "0",
                "servicelevelperf": "42.3",
                "servicelevelperf2": "27.5",
                "weight": "0",
                "max": "100"
            }
        )

    def test_list_queues_no_queues_found(self):
        # Mock the dependency
        app.dependency_overrides[get_ami_manager] = lambda: self.mock

        # Mock the AMI response for no queues
        messages = [
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' EventList='start' Message='Queue status will follow' Response='Success' content=''>",
            "<Message ActionID='action/ff215f4a-5274-4e7d-a89b-9d7a66385a5e/1/2' Event='QueueStatusComplete' EventList='Complete' ListItems='114' content=''>"
        ]
        self.mock.send_action.return_value = list_messages(messages)

        response = self.client.get("/api/v1/queues/")

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            "Response status code should be 200 OK"
        )
        self.assertDictEqual(
            response.json(),
            {"detail": "No queues found"}
        )

    def test_show_queue_found(self):
        # Mock the dependency
        app.dependency_overrides[get_ami_manager] = lambda: self.mock

        # Mock the AMI response for a specific queue
        messages = [
            "<Message ActionID='action/ea92edb2-899c-46e9-89b1-bc7e5e7f97f5/1/7' EventList='start' Message='Queue status will follow' Response='Success' content=''>",
            "<Message Abandoned='14' ActionID='action/ea92edb2-899c-46e9-89b1-bc7e5e7f97f5/1/7' Calls='0' Completed='26' Event='QueueParams' Holdtime='3' Max='100' Queue='Q5' ServiceLevel='0' ServicelevelPerf='42.3' ServicelevelPerf2='27.5' Strategy='leastrecent' TalkTime='86' Weight='0' content=''>"
        ]

        self.mock.send_action.return_value = list_messages(messages)

        response = self.client.get("/api/v1/queues/Q5/")
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            "Response status code should be 200 OK"
        )
        self.assertDictEqual(
            response.json(),
            {
                "queue": "Q5",
                "strategy": "leastrecent",
                "calls": "0",
                "holdtime": "3",
                "talktime": "86",
                "completed": "26",
                "abandoned": "14",
                "servicelevel": "0",
                "servicelevelperf": "42.3",
                "servicelevelperf2": "27.5",
                "weight": "0",
                "max": "100"
            },
            "Response data should match the expected queue details"
        )

    def test_show_queue_not_found(self):
        # Mock the dependency
        app.dependency_overrides[get_ami_manager] = lambda: self.mock

        # Mock the AMI response for a non-existing queue
        messages = [
            "<Message ActionID='action/cc4ced9e-1c43-4053-b8e3-38c5d4ec5d11/1/44' EventList='start' Message='Queue status will follow' Response='Success' content=''>",
            "<Message ActionID='action/cc4ced9e-1c43-4053-b8e3-38c5d4ec5d11/1/44' Event='QueueStatusComplete' EventList='Complete' ListItems='0' content=''>"
        ]
        self.mock.send_action.return_value = list_messages(messages)

        response = self.client.get("/api/v1/queues/Q99/")
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            "Response status code should be 404 Not Found"
        )
        self.assertDictEqual(
            response.json(),
            {"detail": "Queue 'Q99' not found"}
        )

    def test_in_queues_success(self):
        # Mock the dependency
        app.dependency_overrides[get_ami_manager] = lambda: self.mock

        # Mock the AMI response for in-queues
        messages = [
            [
                "<Message ActionID='action/80acc790-3ffb-4119-b077-fd65168226c9/1/2' EventList='start' Message='Queue status will follow' Response='Success' content=''>",
                "<Message Abandoned='0' ActionID='action/80acc790-3ffb-4119-b077-fd65168226c9/1/2' Calls='0' Completed='0' Event='QueueParams' Holdtime='0' Max='100' Queue='Q8' ServiceLevel='0' ServicelevelPerf='0.0' ServicelevelPerf2='0.0' Strategy='leastrecent' TalkTime='0' Weight='0' content=''>",
                "<Message ActionID='action/80acc790-3ffb-4119-b077-fd65168226c9/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2017' LoginTime='1751563002' Membership='dynamic' Name='luis.burgos' Paused='0' PausedReason='' Penalty='0' Queue='Q8' StateInterface='SIP/2017' Status='5' Wrapuptime='0' content=''>",
                "<Message ActionID='action/80acc790-3ffb-4119-b077-fd65168226c9/1/2' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2014' LoginTime='1752079488' Membership='dynamic' Name='natalia.merchan' Paused='0' PausedReason='' Penalty='0' Queue='Q8' StateInterface='SIP/2014' Status='5' Wrapuptime='0' content=''>",
                "<Message ActionID='action/80acc790-3ffb-4119-b077-fd65168226c9/1/2' Event='QueueStatusComplete' EventList='Complete' ListItems='3' content=''>"
            ], [
                "<Message ActionID='action/80acc790-3ffb-4119-b077-fd65168226c9/1/3' EventList='start' Message='Queue status will follow' Response='Success' content=''>",
                "<Message Abandoned='14' ActionID='action/80acc790-3ffb-4119-b077-fd65168226c9/1/3' Calls='0' Completed='26' Event='QueueParams' Holdtime='3' Max='100' Queue='Q5' ServiceLevel='0' ServicelevelPerf='42.3' ServicelevelPerf2='27.5' Strategy='leastrecent' TalkTime='86' Weight='0' content=''>",
                "<Message ActionID='action/80acc790-3ffb-4119-b077-fd65168226c9/1/3' CallsTaken='0' Event='QueueMember' InCall='0' LastCall='0' LastPause='0' Location='SIP/2034' LoginTime='1751555966' Membership='dynamic' Name='natalia.merchan' Paused='0' PausedReason='' Penalty='0' Queue='Q5' StateInterface='SIP/2034' Status='5' Wrapuptime='0' content=''>",
                "<Message ActionID='action/80acc790-3ffb-4119-b077-fd65168226c9/1/3' Event='QueueStatusComplete' EventList='Complete' ListItems='2' content=''>"
            ]
        ]

        self.mock.send_action.side_effect = [
            list_messages(messages[0]),  # First call for Q8
            list_messages(messages[1])   # Second call for Q5
        ]

        response = self.client.post("/api/v1/queues/in/", json=["Q8", "Q5"])
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            "Response status code should be 200 OK"
        )
        data = response.json()
        self.assertEqual(
            len(data), 2, "There should be 2 queues in the response")
        self.assertDictEqual(
            data[0],
            {
                "queue": "Q8",
                "strategy": "leastrecent",
                "calls": "0",
                "holdtime": "0",
                "talktime": "0",
                "completed": "0",
                "abandoned": "0",
                "servicelevel": "0",
                "servicelevelperf": "0.0",
                "servicelevelperf2": "0.0",
                "weight": "0",
                "max": "100"
            },
            "First queue data should match expected values"
        )
        self.assertDictEqual(
            data[1],
            {
                "queue": "Q5",
                "strategy": "leastrecent",
                "calls": "0",
                "holdtime": "3",
                "talktime": "86",
                "completed": "26",
                "abandoned": "14",
                "servicelevel": "0",
                "servicelevelperf": "42.3",
                "servicelevelperf2": "27.5",
                "weight": "0",
                "max": "100"
            },
            "Second queue data should match expected values"
        )

    def test_in_queues_not_found(self):
        # Mock the dependency
        app.dependency_overrides[get_ami_manager] = lambda: self.mock

        # Mock the AMI response for no queues found
        messages = [
            [
                "<Message ActionID='action/d1ee7e32-5de0-4921-877a-10f1faf15b8e/1/5' EventList='start' Message='Queue status will follow' Response='Success' content=''>",
                "<Message ActionID='action/d1ee7e32-5de0-4921-877a-10f1faf15b8e/1/5' Event='QueueStatusComplete' EventList='Complete' ListItems='0' content=''>"
            ],
            [
                "<Message ActionID='action/d1ee7e32-5de0-4921-877a-10f1faf15b8e/1/6' EventList='start' Message='Queue status will follow' Response='Success' content=''>",
                "<Message ActionID='action/d1ee7e32-5de0-4921-877a-10f1faf15b8e/1/6' Event='QueueStatusComplete' EventList='Complete' ListItems='0' content=''>"
            ]
        ]
        self.mock.send_action.side_effect = [
            list_messages(messages[0]),  # First call for Q99
            list_messages(messages[1])   # Second call for Q1001
        ]

        response = self.client.post(
            "/api/v1/queues/in/", json=["Q99", "Q1001"])
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            "Response status code should be 404 Not Found"
        )
        self.assertDictEqual(
            response.json(),
            {"detail": "No queues found"}
        )
