from dataclasses import dataclass

from app.schemas.responses.sip_peer import SipPeer


@dataclass
class SipPeers:
    """
    Class to handle SIP peers.
    """

    @staticmethod
    def map(items: list[dict]) -> list[SipPeer]:
        """
        List all SIP peers.
        """
        peers_info = []
        for item in items:
            if item.event == 'PeerEntry':
                peers_info.append(SipPeer.model_validate(item))
        return peers_info

    @staticmethod
    def map_details(items: list[dict], peer_name: str) -> SipPeer:
        """
        Get details of a specific SIP peer.
        """
        for item in items:
            if item.event == 'PeerEntry' and item.peer == peer_name:
                return SipPeer.model_validate(item)
        return SipPeer()
