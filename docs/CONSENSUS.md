> This document details the consensus mechanism for MeshChain, designed for a decentralized, offline-first environment where every node is a full peer.

# MeshChain Consensus Mechanism

## 1. Core Philosophy: Longest Valid Chain

MeshChain adopts the **Nakamoto Consensus** model, famously pioneered by Bitcoin. The core principle is simple yet powerful: the **longest valid chain is the canonical truth**. This model is exceptionally well-suited for an environment prone to network partitions, as it provides a clear, deterministic rule for resolving conflicts when disconnected networks eventually reconnect.

All nodes in the network, whether online or offline, follow this primary rule. When presented with multiple, conflicting versions of the blockchain, a node will always prioritize the chain that has the most cumulative proof-of-work (which, in a stable network, corresponds to the longest chain of blocks).

---

## 2. Proof-of-Work (PoW) on ESP32

To prevent network spam and secure the block creation process, MeshChain uses a lightweight Proof-of-Work algorithm. This algorithm is specifically designed to be feasible for low-power devices like the ESP32.

### Algorithm: Hash-to-Time (H2T)

Instead of requiring a hash with a certain number of leading zeros (which is computationally intensive), MeshChain uses a **Hash-to-Time (H2T)** algorithm.

1.  **Block Header**: A new block header is created, including the Merkle root of transactions, the previous block's hash, and a nonce.
2.  **Hashing**: The node repeatedly hashes the block header with an incrementing nonce: `hash(block_header + nonce)`.
3.  **Target**: The goal is to produce a hash that, when interpreted as a number, falls within a certain target range. This target is dynamically adjusted to maintain a consistent block time.
4.  **Difficulty Adjustment**: The difficulty (i.e., the size of the target range) is automatically adjusted every 2,016 blocks (approximately every two weeks) to target an average block time of **10 minutes** across the global network.

This approach ensures that while creating a block requires a modest amount of computational effort, it is not so demanding that it drains the battery or overwhelms the CPU of an ESP32 device.

| Parameter | Value | Rationale |
| :--- | :--- | :--- |
| **Target Block Time** | 10 minutes | A balance between transaction confirmation speed and reducing chain splits (forks). |
| **Difficulty Adjustment** | Every 2,016 blocks | Allows the network to adapt to changes in total hashing power. |
| **PoW Algorithm** | Hash-to-Time (H2T) | Lightweight enough for ESP32 devices while still providing sufficient security against spam. |

---

## 3. Consensus in an Offline Mesh

On a disconnected LoRa mesh network, consensus operates on a local level.

- **Block Creation**: Any node on the mesh can mine a new block when it has collected enough transactions.
- **Block Broadcast**: Once a node finds a valid block, it broadcasts it to all its peers on the mesh network.
- **Local Validation**: Receiving nodes validate the block. If it is valid (correct PoW, valid transactions), they add it to their local copy of the blockchain and begin mining the next block on top of it.

This allows the offline mesh to continue extending its own version of the blockchain, confirming transactions in the `Pending` state, even without internet access.

---

## 4. Reconciling Network Partitions

The true power of the longest-chain rule becomes apparent when network partitions reconcile.

**Scenario**: A remote town's mesh network has been offline for a day, producing 144 blocks (24 hours * 6 blocks/hour). The main internet-connected network has also been producing blocks.

1.  **Reconnection**: A node from the town connects to the internet.
2.  **Chain Comparison**: The node discovers that the global chain is significantly longer and has more cumulative proof-of-work than its local chain.
3.  **Reorganization**: The node abandons its local, shorter chain in favor of the global, longer chain. This process is called a "chain reorganization" or "reorg."
4.  **Transaction Re-evaluation**: All transactions that were in the abandoned local chain are now considered unconfirmed. The node re-evaluates these transactions against the new canonical chain. Valid transactions that were not already included in the global chain are re-broadcast to the network to be included in a future block.

```mermaid
graph TD
    subgraph Global Network
        A[Block 1000] --> B[Block 1001] --> C[Block 1002] --> D[... Block 1144]
    end

    subgraph Offline Mesh (Shorter Chain)
        A --> E[Local Block 1001] --> F[Local Block 1002] --> G[... Local Block 1010]
    end

    subgraph Reconciliation
        H{Node Reconnects} --> I{Compares Chains};
        I -->|Global Chain is Longer| J{Abandons Local Chain};
        J --> K{Adopts Global Chain};
        K --> L{Re-broadcasts Local Transactions};
    end

    G --> H;
    D --> H;
```

This mechanism ensures that the entire MeshChain network will **eventually converge** on a single, consistent history, fulfilling the promise of eventual consistency.

---

## 5. Security Against Attacks

### 51% Attack

Like any PoW-based blockchain, MeshChain is theoretically vulnerable to a 51% attack, where a single entity controls a majority of the network's hashing power. However, the decentralized nature of the network (thousands of small ESP32 devices) makes acquiring this much hash power difficult and expensive.

### Selfish Mining

A miner could attempt to mine a secret chain and only broadcast it once it is longer than the public chain. The longest-chain rule and the inherent latency of LoRa networks provide some mitigation, but this remains a theoretical attack vector, as in all PoW systems.
