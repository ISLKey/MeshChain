"""
MeshChain Node Module

This module orchestrates the core components of a MeshChain node, including
the blockchain, mempool, consensus engine, and P2P network manager.
"""

from meshchain.core.blockchain import Blockchain
from meshchain.core.mempool import Mempool
from meshchain.network.network import P2PManager
from meshchain.staking.staking import StakingManager
from meshchain.core.consensus import DPoPConsensus
from meshchain.core.transaction import Transaction

class Node:
    """
    Represents a full MeshChain node, tying all components together.
    """

    def __init__(self, storage_path: str, transport):
        self.blockchain = Blockchain(storage_path)
        self.mempool = Mempool(self.blockchain)
        self.staking_manager = StakingManager()
        self.consensus = DPoPConsensus(self.staking_manager, self.node_id)
        self.p2p_manager = P2PManager(self.blockchain, transport)

        # Register handlers
        self.p2p_manager.on_transaction_received = self.handle_new_transaction

    def start(self):
        """Starts the node's services."""
        self.p2p_manager.start()
        print("MeshChain node started.")

    def stop(self):
        """Stops the node's services."""
        self.p2p_manager.stop()
        print("MeshChain node stopped.")

    def handle_new_transaction(self, tx_data: dict):
        """
        Handles a new transaction received from the network.
        This method implements the first line of defense against double-spends.
        """
        try:
            # In a real implementation, we would deserialize into a Transaction object
            # For now, we'll assume tx_data is a Transaction object for simplicity
            transaction = Transaction.from_dict(tx_data) # Assumes Transaction has from_dict

            # Attempt to add the transaction to the mempool
            # The mempool will perform UTXO locking and double-spend checks.
            if self.mempool.add_transaction(transaction):
                print(f"Added new transaction to mempool: {transaction.hash().hex()}")
                # If successfully added, broadcast it to other peers
                self.p2p_manager.broadcast("TRANSACTION", transaction.to_dict())
            else:
                print(f"Rejected invalid or double-spend transaction: {transaction.hash().hex()}")

        except Exception as e:
            print(f"Error processing transaction: {e}")

    def create_new_block(self):
        """
        Creates a new block with transactions from the mempool.
        This would be called by the consensus engine (e.g., the DPoP leader).
        """
        transactions = self.mempool.get_transactions_for_block(max_transactions=10)
        if not transactions:
            print("No transactions in mempool to create a block.")
            return None

        # The consensus engine would then create and propose the block
        # For now, this is a placeholder for that logic
        print(f"Creating a new block with {len(transactions)} transactions.")
        # new_block = self.consensus.create_block(transactions)
        # self.p2p_manager.broadcast("BLOCK", new_block.to_dict())

        # After the block is confirmed and added to the chain,
        # the transactions need to be removed from the mempool.
        # self.blockchain.add_block(new_block)
        # for tx in new_block.transactions:
        #     self.mempool.remove_transaction(tx.hash())

