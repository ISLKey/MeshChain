"""
MeshChain Network Module (P2P Full Node)

This module has been refactored to support a generic peer-to-peer network suitable
for a full-node, Proof-of-Work architecture. It is designed to be transport-agnostic,
allowing for different communication layers (like LoRa or MQTT) to be used.
"""

import time
import json
import threading
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List, Callable, Dict, Any

# --- Message Types ---
class MessageType(Enum):
    """Defines the types of messages exchanged between peers."""
    GET_BLOCKS = 1
    BLOCK = 2
    TRANSACTION = 3
    PEERS = 4

# --- Peer and Message Structures ---
@dataclass
class Peer:
    """Represents a peer in the network."""
    address: str  # e.g., IP:port or LoRa node ID
    last_seen: float = field(default_factory=time.time)
    height: int = 0

    def touch(self):
        self.last_seen = time.time()

@dataclass
class NetworkMessage:
    """A generic container for messages sent over the network."""
    msg_type: MessageType
    payload: Any

    def to_json(self) -> str:
        return json.dumps({
            'type': self.msg_type.name,
            'payload': self.payload
        })

    @staticmethod
    def from_json(data: str) -> Optional['NetworkMessage']:
        try:
            obj = json.loads(data)
            msg_type = MessageType[obj['type']]
            return NetworkMessage(msg_type, obj['payload'])
        except (json.JSONDecodeError, KeyError):
            return None

# --- P2P Network Manager ---
class P2PManager:
    """
    Manages peer connections, message broadcasting, and blockchain synchronization.
    """

    def __init__(self, blockchain, transport):
        self.blockchain = blockchain
        self.transport = transport
        self.peers: Dict[str, Peer] = {}
        self.on_transaction_received: Optional[Callable] = None
        self._stop_event = threading.Event()

    def start(self):
        """Starts the P2P manager's background tasks."""
        self.transport.start(self.handle_message)
        threading.Thread(target=self._peer_discovery_loop, daemon=True).start()
        threading.Thread(target=self._sync_loop, daemon=True).start()

    def stop(self):
        """Stops the P2P manager."""
        self._stop_event.set()
        self.transport.stop()

    def handle_message(self, sender_address: str, message_data: str):
        """Handles incoming messages from the transport layer."""
        msg = NetworkMessage.from_json(message_data)
        if not msg:
            return

        peer = self.peers.get(sender_address)
        if peer:
            peer.touch()

        if msg.msg_type == MessageType.TRANSACTION:
            if self.on_transaction_received:
                # In a real implementation, we would deserialize the transaction
                # before passing it to the handler.
                self.on_transaction_received(msg.payload)

        elif msg.msg_type == MessageType.BLOCK:
            # Deserialize and validate the block
            block = Block.from_dict(msg.payload)
            self.blockchain.add_block(block)

        elif msg.msg_type == MessageType.GET_BLOCKS:
            # A peer is requesting blocks from us
            start_height = msg.payload.get('start_height', 0)
            blocks_to_send = self.blockchain.get_blocks_from(start_height)
            for block in blocks_to_send:
                self.send_message(sender_address, MessageType.BLOCK, block.to_dict())

        elif msg.msg_type == MessageType.PEERS:
            # A peer is sharing its peer list with us
            for peer_info in msg.payload:
                self.add_peer(peer_info['address'], peer_info['height'])

    def broadcast(self, msg_type: MessageType, payload: Any):
        """Broadcasts a message to all known peers."""
        message = NetworkMessage(msg_type, payload).to_json()
        for peer_address in self.peers.keys():
            self.transport.send(peer_address, message)

    def send_message(self, address: str, msg_type: MessageType, payload: Any):
        """Sends a direct message to a specific peer."""
        message = NetworkMessage(msg_type, payload).to_json()
        self.transport.send(address, message)

    def add_peer(self, address: str, height: int = 0):
        """Adds a new peer to the manager."""
        if address not in self.peers:
            self.peers[address] = Peer(address=address, height=height)

    def _peer_discovery_loop(self):
        """Periodically broadcasts our peer list to discover new peers."""
        while not self._stop_event.is_set():
            peer_list = [{'address': p.address, 'height': p.height} for p in self.peers.values()]
            self.broadcast(MessageType.PEERS, peer_list)
            time.sleep(60)  # Broadcast every minute

    def _sync_loop(self):
        """Periodically attempts to sync the blockchain with peers."""
        while not self._stop_event.is_set():
            if not self.peers:
                time.sleep(10)
                continue

            # Find the peer with the highest block height
            best_peer = max(self.peers.values(), key=lambda p: p.height)
            our_height = self.blockchain.get_latest_block().height

            if best_peer.height > our_height:
                print(f"Syncing from peer {best_peer.address} (height {best_peer.height})")
                self.send_message(
                    best_peer.address,
                    MessageType.GET_BLOCKS,
                    {'start_height': our_height + 1}
                )

            time.sleep(30) # Sync every 30 seconds

# Note: This is a simplified P2P implementation. A real-world version would need
# to handle many more edge cases, such as peer scoring, banning malicious peers,
# more sophisticated sync logic, and a transport-agnostic interface.
