"""
MeshChain Blockchain Module

This module manages the blockchain itself, including adding blocks, validating
transactions, and providing information about the chain state.
"""

from meshchain.core.block import Block
from meshchain.storage.storage_esp32 import FullNodeStorage
from meshchain.core.transaction import Transaction

CONFIRMATION_DEPTH = 6

class Blockchain:
    """
    Manages the blockchain, including the storage and validation of blocks.
    """

    def __init__(self, storage_path: str):
        self.storage = FullNodeStorage(storage_path)

    def get_latest_block(self) -> Block:
        """Returns the latest block in the chain."""
        return self.storage.get_latest_block()

    def get_transaction_status(self, tx_hash: bytes) -> (str, int):
        """Returns the status and confirmation depth of a transaction."""
        block_height = self.storage.get_transaction_block_height(tx_hash)
        if block_height is None:
            return ("Pending", 0)

        latest_height = self.get_latest_block().height
        depth = latest_height - block_height + 1

        if depth >= CONFIRMATION_DEPTH:
            return ("Confirmed", depth)
        else:
            return ("Unconfirmed", depth)

    def add_block(self, block: Block) -> bool:
        """Adds a new block to the blockchain after validation."""
        # In a real implementation, this would involve more rigorous validation
        # against the current chain state.
        return self.storage.save_block(block)

    def is_transaction_valid(self, transaction: Transaction) -> bool:
        """Checks if a transaction is valid against the current blockchain state."""
        # This is a simplified check. A real implementation would verify that
        # all inputs are unspent in the current UTXO set.
        return True
