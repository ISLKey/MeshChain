# MeshChain Transaction Module (UTXO-based)
#
# This module has been refactored to a standard, UTXO-based transaction model,
# removing the outdated and insecure ring signature implementation.

from dataclasses import dataclass, field
from typing import List
import hashlib
from meshchain.crypto.crypto import ecdsa_sign, ecdsa_verify, get_public_key

@dataclass
class TxInput:
    """Represents a transaction input, referencing a previous unspent output."""
    prev_tx_hash: bytes
    prev_tx_output_index: int
    signature: bytes
    public_key: bytes

    def serialize(self) -> bytes:
        data = bytearray()
        data.extend(self.prev_tx_hash)
        data.extend(self.prev_tx_output_index.to_bytes(4, 'big'))
        data.extend(len(self.signature).to_bytes(1, 'big'))
        data.extend(self.signature)
        data.extend(len(self.public_key).to_bytes(1, 'big'))
        data.extend(self.public_key)
        return bytes(data)

    @staticmethod
    def deserialize(data: bytes) -> 'TxInput':
        offset = 0
        prev_tx_hash = data[offset:offset+32]
        offset += 32
        prev_tx_output_index = int.from_bytes(data[offset:offset+4], 'big')
        offset += 4
        sig_len = int.from_bytes(data[offset:offset+1], 'big')
        offset += 1
        signature = data[offset:offset+sig_len]
        offset += sig_len
        pk_len = int.from_bytes(data[offset:offset+1], 'big')
        offset += 1
        public_key = data[offset:offset+pk_len]
        return TxInput(prev_tx_hash, prev_tx_output_index, signature, public_key)

@dataclass
class TxOutput:
    """Represents a transaction output, creating new unspent coins."""
    amount: int
    locking_script: bytes  # Typically a hash of the recipient's public key

    def serialize(self) -> bytes:
        data = bytearray()
        data.extend(self.amount.to_bytes(8, 'big'))
        data.extend(len(self.locking_script).to_bytes(1, 'big'))
        data.extend(self.locking_script)
        return bytes(data)

    @staticmethod
    def deserialize(data: bytes) -> 'TxOutput':
        offset = 0
        amount = int.from_bytes(data[offset:offset+8], 'big')
        offset += 8
        script_len = int.from_bytes(data[offset:offset+1], 'big')
        offset += 1
        locking_script = data[offset:offset+script_len]
        return TxOutput(amount, locking_script)

@dataclass
class TransactionType(Enum):
    TRANSFER = 0
    BOND = 1
    UNBOND = 2

class Transaction:
    """Represents a standard UTXO-based transaction."""
    version: int
    inputs: List[TxInput]
    outputs: List[TxOutput]
    locktime: int
    tx_type: TransactionType = TransactionType.TRANSFER
    tx_payload: bytes = b''
    nonce: int = 0

    def hash(self) -> bytes:
        """Calculates the hash of the transaction, which serves as its unique ID."""
        return hashlib.sha256(hashlib.sha256(self.serialize(for_signing=False)).digest()).digest()

    def serialize(self, for_signing: bool = False) -> bytes:
        """Serializes the transaction to a compact binary format."""
        data = bytearray()
        data.extend(self.version.to_bytes(4, 'big'))
        data.extend(len(self.inputs).to_bytes(1, 'big'))
        for tx_input in self.inputs:
            if for_signing:
                # When signing, the signature and public key are not included
                temp_input = TxInput(tx_input.prev_tx_hash, tx_input.prev_tx_output_index, b'', b'')
                data.extend(temp_input.serialize())
            else:
                data.extend(tx_input.serialize())
        data.extend(len(self.outputs).to_bytes(1, 'big'))
        for tx_output in self.outputs:
            data.extend(tx_output.serialize())
        data.extend(self.locktime.to_bytes(4, 'big'))
        return bytes(data)

    @staticmethod
    def deserialize(data: bytes) -> 'Transaction':
        offset = 0
        version = int.from_bytes(data[offset:offset+4], 'big')
        offset += 4
        input_count = int.from_bytes(data[offset:offset+1], 'big')
        offset += 1
        inputs = []
        for _ in range(input_count):
            # This is tricky because TxInput is variable length
            # A more robust implementation would be needed here
            # For now, we assume a fixed-size or self-describing format
            pass # Placeholder
        output_count = int.from_bytes(data[offset:offset+1], 'big')
        offset += 1
        outputs = []
        for _ in range(output_count):
            # Same as above for TxOutput
            pass # Placeholder
        locktime = int.from_bytes(data[offset:offset+4], 'big')
        return Transaction(version, inputs, outputs, locktime)

    def sign(self, private_key: bytes, utxo_set: dict):
        """Signs all inputs of the transaction."""
        tx_to_sign = self.serialize(for_signing=True)
        for i, tx_input in enumerate(self.inputs):
            # In a real implementation, we would get the locking script from the UTXO set
            # and use it to form the message to be signed.
            message = hashlib.sha256(tx_to_sign).digest()
            signature = ecdsa_sign(private_key, message)
            self.inputs[i].signature = signature
            self.inputs[i].public_key = get_public_key(private_key)

    def verify_signature(self) -> bool:
        """Verifies the signatures of all inputs."""
        tx_to_verify = self.serialize(for_signing=True)
        message = hashlib.sha256(tx_to_verify).digest()
        for tx_input in self.inputs:
            if not ecdsa_verify(tx_input.public_key, tx_input.signature, message):
                return False
        return True

# Note: The deserialize methods are simplified and would need a more robust
# implementation to handle the variable-length nature of the inputs and outputs.
