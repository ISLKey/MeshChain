# MeshChain Block Module (Proof-of-Work)
#
# This module has been refactored to align with the new unified node architecture
# and Nakamoto consensus (Proof-of-Work).

from dataclasses import dataclass, field
from typing import List
import hashlib
import time
from meshchain.core.transaction import Transaction

@dataclass
class Block:
    """
    Represents a MeshChain block, designed for a Proof-of-Work consensus mechanism.

    Attributes:
        version: Protocol version.
        height: The block number in the blockchain.
        timestamp: The time the block was created.
        previous_hash: The hash of the preceding block.
        merkle_root: The root hash of the block's transaction Merkle tree.
        difficulty: The difficulty target for this block's PoW.
        nonce: The nonce found to satisfy the PoW difficulty.
        transactions: A list of transactions included in the block.
    """

    version: int
    height: int
    timestamp: int
    previous_hash: bytes
    merkle_root: bytes
    difficulty: int
    nonce: int
    transactions: List[Transaction] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate block fields after initialization."""
        if self.version < 0 or self.version > 255:
            raise ValueError("Version must be between 0 and 255")
        if self.height < 0:
            raise ValueError("Height must be a non-negative integer")
        if len(self.previous_hash) != 32:
            raise ValueError("Previous hash must be 32 bytes")
        if len(self.merkle_root) != 32:
            raise ValueError("Merkle root must be 32 bytes")

    def header_hash(self) -> bytes:
        """Calculates the hash of the block header, which is used for PoW."""
        header = (
            self.version.to_bytes(1, 'big') +
            self.height.to_bytes(4, 'big') +
            self.timestamp.to_bytes(8, 'big') +
            self.previous_hash +
            self.merkle_root +
            self.difficulty.to_bytes(4, 'big') +
            self.nonce.to_bytes(8, 'big')
        )
        return hashlib.sha256(hashlib.sha256(header).digest()).digest()

    def serialize(self) -> bytes:
        """Serializes the entire block to a compact binary format."""
        data = bytearray()
        data.extend(self.version.to_bytes(1, 'big'))
        data.extend(self.height.to_bytes(4, 'big'))
        data.extend(self.timestamp.to_bytes(8, 'big'))
        data.extend(self.previous_hash)
        data.extend(self.merkle_root)
        data.extend(self.difficulty.to_bytes(4, 'big'))
        data.extend(self.nonce.to_bytes(8, 'big'))
        data.extend(len(self.transactions).to_bytes(4, 'big'))
        for tx in self.transactions:
            tx_data = tx.serialize()
            data.extend(len(tx_data).to_bytes(4, 'big'))
            data.extend(tx_data)
        return bytes(data)

    @staticmethod
    def deserialize(data: bytes) -> 'Block':
        """Deserializes a block from its binary format."""
        offset = 0
        version = int.from_bytes(data[offset:offset+1], 'big')
        offset += 1
        height = int.from_bytes(data[offset:offset+4], 'big')
        offset += 4
        timestamp = int.from_bytes(data[offset:offset+8], 'big')
        offset += 8
        previous_hash = data[offset:offset+32]
        offset += 32
        merkle_root = data[offset:offset+32]
        offset += 32
        difficulty = int.from_bytes(data[offset:offset+4], 'big')
        offset += 4
        nonce = int.from_bytes(data[offset:offset+8], 'big')
        offset += 8
        tx_count = int.from_bytes(data[offset:offset+4], 'big')
        offset += 4
        transactions = []
        for _ in range(tx_count):
            tx_size = int.from_bytes(data[offset:offset+4], 'big')
            offset += 4
            tx_data = data[offset:offset+tx_size]
            transactions.append(Transaction.deserialize(tx_data))
            offset += tx_size
        return Block(
            version=version, height=height, timestamp=timestamp,
            previous_hash=previous_hash, merkle_root=merkle_root,
            difficulty=difficulty, nonce=nonce, transactions=transactions
        )

    def calculate_merkle_root(self) -> bytes:
        """Calculates the Merkle root of the block's transactions."""
        if not self.transactions:
            return b'\x00' * 32
        tx_hashes = [tx.hash() for tx in self.transactions]
        while len(tx_hashes) > 1:
            if len(tx_hashes) % 2 != 0:
                tx_hashes.append(tx_hashes[-1])
            new_hashes = []
            for i in range(0, len(tx_hashes), 2):
                combined = tx_hashes[i] + tx_hashes[i+1]
                new_hash = hashlib.sha256(hashlib.sha256(combined).digest()).digest()
                new_hashes.append(new_hash)
            tx_hashes = new_hashes
        return tx_hashes[0]

    def is_valid(self) -> bool:
        """Validates the block's structure and integrity."""
        if self.calculate_merkle_root() != self.merkle_root:
            return False
        for tx in self.transactions:
            if not tx.verify_signature():
                return False
        return True

    def __repr__(self) -> str:
        """Returns a string representation of the block."""
        return (
            f"Block(height={self.height}, "
            f"hash={self.header_hash().hex()}, "
            f"txs={len(self.transactions)})"
        )

# Example usage:
if __name__ == "__main__":
    # This example requires a valid Transaction class.
    # The following is a placeholder for demonstration.
    class PlaceholderTransaction:
        def serialize(self): return b'tx_data'
        def hash(self): return hashlib.sha256(b'tx_data').digest()
        def verify_signature(self): return True
        @staticmethod
        def deserialize(data): return PlaceholderTransaction()

    # Replace PlaceholderTransaction with the actual Transaction class when available
    Transaction = PlaceholderTransaction

    block = Block(
        version=1,
        height=1,
        timestamp=int(time.time()),
        previous_hash=b'\x00' * 32,
        merkle_root=b'\x00' * 32,
        difficulty=1,
        nonce=0,
        transactions=[Transaction()]
    )
    block.merkle_root = block.calculate_merkle_root()

    print(f"Block: {block}")
    print(f"Hash: {block.header_hash().hex()}")

    serialized = block.serialize()
    print(f"Serialized size: {len(serialized)} bytes")

    deserialized = Block.deserialize(serialized)
    print(f"Deserialized: {deserialized}")
    print(f"Hashes match: {block.header_hash() == deserialized.header_hash()}")
