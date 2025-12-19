> This document outlines the security model of MeshChain, including cryptographic foundations, common attack vectors, and mitigation strategies. It is based on the unified node architecture where every node is a full peer.

# MeshChain Security Model

## 1. Cryptographic Suite

MeshChain relies on a foundation of modern, well-vetted cryptography to secure user funds and network communications.

### Ed25519 for Digital Signatures

All standard transactions are signed using the **Ed25519** signature algorithm. 

- **Function**: It is used to prove ownership of funds. When a user sends a transaction, they sign it with their private key. This signature proves they authorized the transaction without revealing the private key itself.
- **Security**: Ed25519 is widely considered to be secure, efficient, and resistant to many of the side-channel attacks that can affect other signature schemes. It provides a 128-bit security level.
- **Implementation**: A constant-time, audited implementation is used to prevent timing attacks on the ESP32 platform.

### Stealth Addresses for Privacy

To enhance user privacy, MeshChain uses **stealth addresses**. When you send funds to a recipient, you don't send them to their public address directly. Instead, you derive a new, one-time address for that specific transaction. Only the sender and receiver can determine that the transaction belongs to the recipient's wallet.

- **Mechanism**: This is achieved using Elliptic Curve Diffie-Hellman (ECDH) key exchange. The sender uses their private key and the recipient's public key to compute a shared secret, which is then used to generate the unique, one-time address.
- **Benefit**: This makes it computationally infeasible for an outside observer to link multiple transactions to the same recipient, significantly improving privacy on a public ledger.

### Ring Signatures (Under Review)

An earlier version of MeshChain included a custom implementation of ring signatures for transaction mixing and sender anonymity. However, a security audit revealed critical flaws in this implementation.

- **Current Status**: The ring signature feature is **disabled** pending a complete security overhaul.
- **Path Forward**: The plan is to replace the flawed custom code with a well-audited, mainstream implementation of a privacy-enhancing technology, such as RingCT (as used in Monero) or a similar zero-knowledge proof system adapted for the ESP32's constraints.

| Cryptographic Primitive | Purpose | Status |
| :--- | :--- | :--- |
| **Ed25519 Signatures** | Transaction Authorization | **Active & Secure** |
| **Stealth Addresses** | Recipient Privacy | **Active & Secure** |
| **Ring Signatures** | Sender Anonymity | **Disabled & Under Review** |

---

## 2. Wallet Security

Wallet security is paramount. The user's private keys are generated and stored directly on the ESP32 device.

- **Key Generation**: Private keys are generated using a cryptographically secure random number generator (CSPRNG), seeded with entropy from the ESP32's hardware random number generator.
- **Storage**: Private keys are stored in the encrypted NVS (Non-Volatile Storage) partition of the ESP32's flash memory. 
- **Backup & Restore**: Users are provided with a 24-word mnemonic seed phrase (BIP39 compatible) during wallet creation. This phrase can be used to restore the wallet on any other MeshChain-compatible device. **It is the user's responsibility to store this seed phrase securely.**

---

## 3. Network Attack Vectors & Mitigation

### Sybil Attack

- **Attack**: An adversary creates a large number of fake nodes (identities) to gain a disproportionate influence on the network.
- **Mitigation**: The Proof-of-Work (PoW) consensus mechanism serves as the primary defense. To create blocks and influence the chain, an attacker must expend real-world computational resources. Creating fake identities is easy, but contributing to the blockchain's history requires significant hashing power, making Sybil attacks economically infeasible to sustain.

### Eclipse Attack

- **Attack**: An attacker isolates a specific node from the rest of the network, controlling all its incoming and outgoing connections. This allows the attacker to feed the victim false information (e.g., a fake blockchain).
- **Mitigation**: The LoRa mesh topology provides natural resistance. A node typically has multiple peers within radio range. For an attacker to successfully eclipse a node, they would need to physically surround it and overpower the signals from all legitimate neighbors. Additionally, nodes periodically attempt to discover new peers, making long-term isolation difficult.

### 51% Attack

- **Attack**: An attacker controlling a majority of the network's hashing power can unilaterally dictate the blockchain's history, enabling double-spending and transaction censorship.
- **Mitigation**: There is no perfect defense against a 51% attack in a PoW system. MeshChain's security relies on the economic assumption that it would be prohibitively expensive to acquire and operate enough ESP32 devices to dominate the thousands of honest nodes participating in the network.

### Replay Attacks

- **Attack**: An attacker intercepts a valid transaction and re-broadcasts it to the network to make it execute a second time.
- **Mitigation**: This is prevented by the core design of the blockchain. Once a transaction is included in a block, it is considered part of the ledger's history. Any attempt to include the exact same transaction in a future block will be rejected by all nodes as a duplicate.

---

## 4. Two-Level Confirmation and Security

The two-level confirmation system has important security implications:

- **`Pending` Transactions**: These are not final. Users should treat them as such. For high-value transactions, it is crucial to wait for `Confirmed` status. This is analogous to waiting for multiple confirmations in Bitcoin.
- **Double-Spend Risk (Offline)**: In an isolated mesh, a malicious actor could broadcast a transaction to one group of peers and a conflicting transaction (a double-spend) to another group. This conflict will only be resolved when the partition reconnects to the global network and one of the transactions is invalidated. This is an inherent risk of offline operation.
