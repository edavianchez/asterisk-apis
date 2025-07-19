
import unittest
from unittest.mock import AsyncMock, MagicMock
from fastapi import status
from fastapi.testclient import TestClient
from main import app
from app.dependencies import get_ami_manager
from app.core.config import settings
from tests.dependencies import list_messages, create_test_jwt


class SipPeersApiTests(unittest.TestCase):
    def setUp(self):
        token = create_test_jwt()
        self.client = TestClient(
            app,
            base_url=settings.app_url,
            headers={"Authorization": f"Bearer {token}"}
        )
        self.mock = MagicMock()
        self.mock.send_action = AsyncMock()
        # Mock the dependency
        app.dependency_overrides[get_ami_manager] = lambda: self.mock

    def tearDown(self):
        app.dependency_overrides = {}

    def test_list_sip_peers_success(self):

        # Mock the AMI response
        messages = [
            "<Message ActionID='action/df27bd53-9e29-44a9-a781-449d919140c2/1/2' EventList='start' Message='Peer status list will follow' Response='Success' content=''>",
            "<Message ACL='no' Accountcode='1000' ActionID='action/df27bd53-9e29-44a9-a781-449d919140c2/1/2' AutoComedia='no' AutoForcerport='no' ChanObjectType='peer' Channeltype='SIP' Comedia='yes' Description='' Dynamic='yes' Event='PeerEntry' Forcerport='yes' IPaddress='-none-' IPport='0' ObjectName='1000' RealtimeDevice='no' Status='UNKNOWN' TextSupport='no' VideoSupport='no' content=''>",
            "<Message ACL='no' Accountcode='1002' ActionID='action/df27bd53-9e29-44a9-a781-449d919140c2/1/2' AutoComedia='no' AutoForcerport='no' ChanObjectType='peer' Channeltype='SIP' Comedia='yes' Description='' Dynamic='yes' Event='PeerEntry' Forcerport='yes' IPaddress='-none-' IPport='0' ObjectName='1002' RealtimeDevice='no' Status='UNKNOWN' TextSupport='no' VideoSupport='no' content=''>",
            "<Message ACL='no' Accountcode='1110' ActionID='action/df27bd53-9e29-44a9-a781-449d919140c2/1/2' AutoComedia='no' AutoForcerport='no' ChanObjectType='peer' Channeltype='SIP' Comedia='yes' Description='' Dynamic='yes' Event='PeerEntry' Forcerport='yes' IPaddress='-none-' IPport='0' ObjectName='1110' RealtimeDevice='no' Status='UNKNOWN' TextSupport='no' VideoSupport='no' content=''>", "<Message ACL='no' ActionID='action/df27bd53-9e29-44a9-a781-449d919140c2/1/2' AutoComedia='no' AutoForcerport='no' ChanObjectType='peer' Channeltype='SIP' Comedia='yes' Description='' Dynamic='no' Event='PeerEntry' Forcerport='yes' IPaddress='172.17.8.203' IPport='5060' ObjectName='PXY203' RealtimeDevice='no' Status='OK (1 ms)' TextSupport='no' VideoSupport='no' content=''>",
            "<Message ACL='no' ActionID='action/df27bd53-9e29-44a9-a781-449d919140c2/1/2' AutoComedia='no' AutoForcerport='no' ChanObjectType='peer' Channeltype='SIP' Comedia='yes' Description='' Dynamic='no' Event='PeerEntry' Forcerport='yes' IPaddress='10.57.251.80' IPport='5060' ObjectName='PXY30' RealtimeDevice='no' Status='OK (1 ms)' TextSupport='no' VideoSupport='no' content=''>",
            "<Message ACL='no' ActionID='action/df27bd53-9e29-44a9-a781-449d919140c2/1/2' AutoComedia='no' AutoForcerport='no' ChanObjectType='peer' Channeltype='SIP' Comedia='yes' Description='' Dynamic='no' Event='PeerEntry' Forcerport='yes' IPaddress='10.57.251.82' IPport='5060' ObjectName='PXY7105' RealtimeDevice='no' Status='OK (1 ms)' TextSupport='no' VideoSupport='no' content=''>",
            "<Message ACL='no' ActionID='action/df27bd53-9e29-44a9-a781-449d919140c2/1/2' AutoComedia='no' AutoForcerport='no' ChanObjectType='peer' Channeltype='SIP' Comedia='yes' Description='' Dynamic='no' Event='PeerEntry' Forcerport='yes' IPaddress='10.57.251.80' IPport='5060' ObjectName='PXY730' RealtimeDevice='no' Status='OK (1 ms)' TextSupport='no' VideoSupport='no' content=''>",
            "<Message ACL='no' ActionID='action/df27bd53-9e29-44a9-a781-449d919140c2/1/2' AutoComedia='no' AutoForcerport='no' ChanObjectType='peer' Channeltype='SIP' Comedia='yes' Description='' Dynamic='no' Event='PeerEntry' Forcerport='yes' IPaddress='10.57.251.179' IPport='5060' ObjectName='VC11179' RealtimeDevice='no' Status='OK (1 ms)' TextSupport='no' VideoSupport='no' content=''>",
            "<Message ACL='no' ActionID='action/df27bd53-9e29-44a9-a781-449d919140c2/1/2' AutoComedia='no' AutoForcerport='no' ChanObjectType='peer' Channeltype='SIP' Comedia='yes' Description='' Dynamic='no' Event='PeerEntry' Forcerport='yes' IPaddress='10.57.251.181' IPport='5060' ObjectName='VC11181' RealtimeDevice='no' Status='OK (1 ms)' TextSupport='no' VideoSupport='no' content=''>",
            "<Message ACL='no' ActionID='action/df27bd53-9e29-44a9-a781-449d919140c2/1/2' AutoComedia='no' AutoForcerport='no' ChanObjectType='peer' Channeltype='SIP' Comedia='yes' Description='' Dynamic='no' Event='PeerEntry' Forcerport='yes' IPaddress='172.17.8.206' IPport='5060' ObjectName='VC206' RealtimeDevice='no' Status='OK (1 ms)' TextSupport='no' VideoSupport='no' content=''>",
            "<Message ACL='no' ActionID='action/df27bd53-9e29-44a9-a781-449d919140c2/1/2' AutoComedia='no' AutoForcerport='no' ChanObjectType='peer' Channeltype='SIP' Comedia='yes' Description='' Dynamic='no' Event='PeerEntry' Forcerport='yes' IPaddress='172.17.8.205' IPport='5060' ObjectName='VC8205' RealtimeDevice='no' Status='OK (1 ms)' TextSupport='no' VideoSupport='no' content=''>",
            "<Message ACL='no' ActionID='action/df27bd53-9e29-44a9-a781-449d919140c2/1/2' AutoComedia='no' AutoForcerport='no' ChanObjectType='peer' Channeltype='SIP' Comedia='yes' Description='' Dynamic='no' Event='PeerEntry' Forcerport='yes' IPaddress='172.17.8.87' IPport='5060' ObjectName='VC887' RealtimeDevice='no' Status='OK (1 ms)' TextSupport='no' VideoSupport='no' content=''>",
            "<Message ACL='no' Accountcode='gs102' ActionID='action/df27bd53-9e29-44a9-a781-449d919140c2/1/2' AutoComedia='no' AutoForcerport='no' ChanObjectType='peer' Channeltype='SIP' Comedia='yes' Description='' Dynamic='yes' Event='PeerEntry' Forcerport='yes' IPaddress='-none-' IPport='0' ObjectName='gs102' RealtimeDevice='no' Status='UNKNOWN' TextSupport='no' VideoSupport='no' content=''>",
            "<Message ActionID='action/df27bd53-9e29-44a9-a781-449d919140c2/1/2' Event='PeerlistComplete' EventList='Complete' ListItems='141' content=''>"
        ]
        self.mock.send_action.return_value = list_messages(messages)

        response = self.client.get("/api/v1/sip_peers/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            "Response status code should be 200 OK"
        )
        self.assertDictEqual(
            response.json()[0],
            {
                "objectname": "1000",
                "ipaddress": "-none-",
                "ipport": 0,
                "status": "UNKNOWN"
            },
            "Response should contain SIP peer details"
        )

    def test_list_sip_peers_no_peers_found(self):
        # Mock the AMI response for no peers
        messages = [
            "<Message ActionID='action/df27bd53-9e29-44a9-a781-449d919140c2/1/2' EventList='start' Message='Peer status list will follow' Response='Success' content=''>",
            "<Message ActionID='action/df27bd53-9e29-44a9-a781-449d919140c2/1/2' Event='PeerlistComplete' EventList='Complete' ListItems='141' content=''>"
        ]
        self.mock.send_action.return_value = list_messages(messages)

        response = self.client.get("/api/v1/sip_peers/")

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            "Response status code should be 404 Not Found"
        )
        self.assertDictEqual(
            response.json(),
            {'detail': 'No SIP peers found'},
            "Error response should contain 'No SIP peers found' message"
        )
