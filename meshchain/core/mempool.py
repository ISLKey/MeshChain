"""
MeshChain Mempool Module

This module manages the pool of unconfirmed transactions, providing a critical
defense against double-spending by implementing UTXO locking.
"""

import threading
from typing import Dict, List, Set

from meshchain.core.transaction import Transaction, TxInput
from collections import defaultdict

class Mempool:
    """
    Manages unconfirmed transactions and prevents double-spends within the local
    node's view of the network.
    """

    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.transactions: Dict[bytes, Transaction] = {}
        self.spent_utxos: Set[bytes] = set()
        self.account_nonces: Dict[bytes, int] = defaultdict(int)
        self.lock = threading.Lock()

    def add_transaction(self, transaction: Transaction) -> bool:
        """Adds a transaction to the mempool after validation."""
        with self.lock:
            if transaction.hash() in self.transactions:
                return False  # Already in mempool

            # 1. Basic transaction validation
            if not transaction.verify_signature():
                return False

            # 2. Check for double-spends against the blockchain
            if not self.blockchain.is_transaction_valid(transaction):
                return False

            # 4. Check for valid nonce
            sender_pub_key = transaction.inputs[0].public_key # Simplified: assumes one sender
            if transaction.nonce <= self.account_nonces[sender_pub_key]:
                return False # Replay attack or out of order
                return False

            # 3. Check for double-spends against the mempool (UTXO locking)
            for tx_input in transaction.inputs:
                utxo_id = self._get_utxo_id(tx_input)
                if utxo_id in self.spent_utxos:
                    return False  # Double-spend attempt

            # Add the transaction and lock its UTXOs
            self.transactions[transaction.hash()] = transaction
            for tx_input in transaction.inputs:
                self.spent_utxos.add(self._get_utxo_id(tx_input))

            return True

    def remove_transaction(self, transaction_hash: bytes):
        """Removes a transaction from the mempool, typically after it has been mined."""
        with self.lock:
            if transaction_hash in self.transactions:
                transaction = self.transactions.pop(transaction_hash)
                for tx_input in transaction.inputs:
                    utxo_id = self._get_utxo_id(tx_input)
                    if utxo_id in self.spent_utxos:
                        self.spent_utxos.remove(utxo_id)

    def get_transactions_for_block(self, max_transactions: int) -> List[Transaction]:
        """Returns a list of transactions to be included in a new block."""
        with self.lock:
            # A more sophisticated implementation would prioritize by fee
            return list(self.transactions.values())[:max_transactions]

    def _get_utxo_id(self, tx_input: TxInput) -> bytes:
        """Generates a unique identifier for a UTXO."""
        return tx_input.prev_tx_hash + tx_input.prev_tx_output_index.to_bytes(4, 'big')
