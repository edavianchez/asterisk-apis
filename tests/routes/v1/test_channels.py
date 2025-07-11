
import unittest
from app.core.config import settings
from app.dependencies import get_ami_manager
from fastapi import status
from fastapi.testclient import TestClient
from main import app
from unittest.mock import AsyncMock, MagicMock

from tests.dependencies import list_messages


class ChannelsApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app, base_url=settings.app_url)
        self.mock = MagicMock()
        self.mock.send_action = AsyncMock()

    def tearDown(self):
        app.dependency_overrides = {}

    def test_list_channels_success(self):
        # Mock the dependency
        app.dependency_overrides[get_ami_manager] = lambda: self.mock

        # Mock the AMI response
        messages = [
            "<Message ActionID='action/14b341a7-5360-4f4b-84a5-cd759a636b35/1/10' EventList='start' Message='Channels will follow' Response='Success' content=''>",
            "<Message AccountCode='' ActionID='action/14b341a7-5360-4f4b-84a5-cd759a636b35/1/10' Application='Queue' ApplicationData='Q1,tT' BridgeId='e8c83cb4-9d01-41c7-a381-2391448d5667' CallerIDName='3cec83fc-4e4b-0fbc-74aa-940c08cf261b' CallerIDNum='3024519966' Channel='SIP/VC8205-00000260' ChannelState='6' ChannelStateDesc='Up' ConnectedLineName='ext 2001' ConnectedLineNum='0000000000' Context='Inbound' Duration='00:00:12' Event='CoreShowChannel' Exten='6014863004' Language='es' Linkedid='1752249341.1112' Priority='29' Uniqueid='1752249341.1112' content=''>",
            "<Message AccountCode='2001' ActionID='action/14b341a7-5360-4f4b-84a5-cd759a636b35/1/10' Application='AppQueue' ApplicationData='(Outgoing Line)' BridgeId='e8c83cb4-9d01-41c7-a381-2391448d5667' CallerIDName='ext 2001' CallerIDNum='0000000000' Channel='SIP/2001-00000261' ChannelState='6' ChannelStateDesc='Up' ConnectedLineName='3cec83fc-4e4b-0fbc-74aa-940c08cf261b' ConnectedLineNum='3024519966' Context='trunkinbound' Duration='00:00:11' Event='CoreShowChannel' Exten='6014863004' Language='en' Linkedid='1752249341.1112' Priority='1' Uniqueid='1752249342.1113' content=''>",
            "<Message ActionID='action/14b341a7-5360-4f4b-84a5-cd759a636b35/1/10' Event='CoreShowChannelsComplete' EventList='Complete' ListItems='2' content=''>"
        ]
        self.mock.send_action.return_value = list_messages(messages)

        response = self.client.get("/api/v1/channels/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            "Response status code should be 200 OK"
        )
        data = response.json()
        self.assertDictEqual(
            response.json()[0],
            {
                "channel": "SIP/VC8205-00000260",
                "channelstate": 6,
                "channelstatedesc": "Up",
                "connectedlinename": "ext 2001",
                "connectedlinenum": "0000000000",
                "context": "Inbound",
                "duration": "00:00:12"
            }
        )

    def test_list_channels_no_channels_found(self):
        # Mock the dependency
        app.dependency_overrides[get_ami_manager] = lambda: self.mock

        # Mock the AMI response for no channels
        messages = [
            "<Message ActionID='action/d1fed037-f5b9-4b69-a8a0-d503d679d500/1/2' EventList='start' Message='Channels will follow' Response='Success' content=''>",
            "<Message ActionID='action/d1fed037-f5b9-4b69-a8a0-d503d679d500/1/2' Event='CoreShowChannelsComplete' EventList='Complete' ListItems='0' content=''>"
        ]
        self.mock.send_action.return_value = list_messages(messages)

        response = self.client.get("/api/v1/channels/")

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            "Error response status code should be 404"
        )
        self.assertDictEqual(
            response.json(),
            {'detail': 'No channels found'},
            "Error response should contain 'No channels found' message"
        )
