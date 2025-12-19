"""
MeshChain Staking and Slashing Module

This module implements the economic security layer of the DPoP consensus
mechanism, including validator bonding, stake management, and slashing for
malicious behavior.
"""

import time
from dataclasses import dataclass, field
from typing import Dict, List

# --- Constants ---
MINIMUM_BOND = 1000  # Minimum stake to become a validator
SLASH_PENALTY_DOUBLE_SIGN = 0.5  # 50% penalty for double-signing
SLASH_PENALTY_DOWNTIME = 0.01  # 1% penalty for being offline

# --- Data Classes ---
@dataclass
class Validator:
    """Represents a validator in the network."""
    node_id: bytes
    bond: int = 0
    is_active: bool = False
    last_seen: float = field(default_factory=time.time)

    def can_validate(self) -> bool:
        return self.is_active and self.bond >= MINIMUM_BOND

@dataclass
class SlashingRecord:
    """Records an instance of a validator being slashed."""
    node_id: bytes
    slashed_amount: int
    reason: str
    timestamp: float = field(default_factory=time.time)

# --- Staking Manager ---
class StakingManager:
    """
    Manages the lifecycle of validators, including their bonds and status.
    """

    def __init__(self):
        self.validators: Dict[bytes, Validator] = {}
        self.slashing_history: List[SlashingRecord] = []

    def add_validator(self, node_id: bytes):
        """Adds a new potential validator to the registry."""
        if node_id not in self.validators:
            self.validators[node_id] = Validator(node_id=node_id)

    def process_bond(self, node_id: bytes, amount: int):
        """Processes a bond transaction, adding to a validator's stake."""
        if node_id not in self.validators:
            self.add_validator(node_id)
        self.validators[node_id].bond += amount
        if self.validators[node_id].bond >= MINIMUM_BOND:
            self.validators[node_id].is_active = True

    def process_unbond(self, node_id: bytes, amount: int):
        """Processes an unbond transaction, reducing a validator's stake."""
        if node_id in self.validators:
            self.validators[node_id].bond = max(0, self.validators[node_id].bond - amount)
            if self.validators[node_id].bond < MINIMUM_BOND:
                self.validators[node_id].is_active = False

    def get_validator(self, node_id: bytes) -> Validator:
        return self.validators.get(node_id)

    def get_active_validators(self) -> List[Validator]:
        """Returns a list of all validators who meet the minimum bond requirement."""
        return [v for v in self.validators.values() if v.can_validate()]

    def slash_validator(self, node_id: bytes, penalty_fraction: float, reason: str):
        """Slashes a validator's bond for misbehavior."""
        if node_id in self.validators:
            validator = self.validators[node_id]
            slashed_amount = int(validator.bond * penalty_fraction)
            validator.bond -= slashed_amount
            validator.is_active = validator.bond >= MINIMUM_BOND

            record = SlashingRecord(node_id, slashed_amount, reason)
            self.slashing_history.append(record)
            print(f"Slashed validator {node_id.hex()}: removed {slashed_amount} for {reason}")

    def check_for_double_signing(self, block1, block2):
        """
        Checks if two blocks were signed by the same validator at the same height.
        This is a simplified check; a real implementation would be more robust.
        """
        if block1.height == block2.height and block1.validator_id == block2.validator_id:
            self.slash_validator(
                block1.validator_id,
                SLASH_PENALTY_DOUBLE_SIGN,
                f"Double-signing at height {block1.height}"
            )
