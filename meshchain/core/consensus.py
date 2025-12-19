"""
MeshChain Consensus Module (DPoP with Roles)

This module implements the Delegated Proof-of-Participation (DPoP) consensus
mechanism, featuring role-based weighting for a unified node model.
"""

import random
from typing import List, Dict

from meshchain.staking.staking import StakingManager, Validator
from meshchain.core.block import Block
from meshchain.core.transaction import Transaction

# --- Role Weights ---
ROLE_WEIGHTS = {
    "User": 1,
    "Validator": 10,
    "Super Validator": 100,
}

class DPoPConsensus:
    """
    Implements the DPoP consensus logic, including leader selection and block validation.
    """

    def __init__(self, staking_manager: StakingManager, node_id: bytes):
        self.staking_manager = staking_manager
        self.node_id = node_id

    def select_leader(self, last_block_hash: bytes) -> bytes:
        """Selects the next block producer based on a weighted random selection."""
        validators = self.staking_manager.get_active_validators()
        if not validators:
            return None

        weighted_list = []
        for validator in validators:
            weight = self._get_validator_weight(validator)
            weighted_list.extend([validator.node_id] * weight)

        # Deterministic random selection based on the last block hash
        seed = int.from_bytes(last_block_hash, 'big')
        random.seed(seed)
        return random.choice(weighted_list)

    def create_block(
        self, transactions: List[Transaction], last_block: Block
    ) -> Block:
        """Creates a new block, to be signed by the current node if it is the leader."""
        leader = self.select_leader(last_block.header_hash())
        if leader != self.node_id:
            print(f"Not our turn to create a block. Leader is {leader.hex()}")
            return None

        # In a real implementation, the block would be constructed here
        # and then signed by the leader.
        print(f"We are the leader! Creating a new block.")
        # new_block = Block(...)
        # new_block.sign(self.private_key)
        # return new_block
        return None # Placeholder

    def validate_block(self, block: Block) -> bool:
        """Validates a new block received from the network."""
        # 1. Check the block producer's signature
        # if not block.verify_signature():
        #     return False

        # 2. Check that the producer was the legitimate leader for this block height
        # leader = self.select_leader(self.blockchain.get_block(block.height - 1).hash())
        # if block.producer_id != leader:
        #     return False

        # 3. All other standard block validations (transactions, etc.)
        return True

    def _get_validator_weight(self, validator: Validator) -> int:
        """Calculates the consensus weight of a validator based on their role."""
        # This is a simplified role determination. A real system would have a more
        # robust way of assigning roles based on stake, uptime, etc.
        if validator.bond > 10000: # Example threshold for Super Validator
            role = "Super Validator"
        elif validator.bond >= 1000: # Example threshold for Validator
            role = "Validator"
        else:
            role = "User"
        
        return ROLE_WEIGHTS[role]
