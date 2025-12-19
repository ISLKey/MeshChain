> This document outlines the future development roadmap for MeshChain. The timeline is ambitious and subject to change based on community feedback and development resources.

# MeshChain Development Roadmap

With the core architecture now solidified, development will proceed in focused phases. The goal is to incrementally build upon the stable foundation, introducing new features while maintaining security and decentralization.

---

## Phase 1: Mainnet Launch & Stabilization (Q1 2026)

This phase is focused on launching the production network and ensuring its stability.

- **[✓] Core Architecture**: Finalize and document the unified node and two-level confirmation system.
- **[✓] Production-Ready Code**: Complete the final implementation of the `micronode` core, storage layer, and async framework.
- **[ ] Mainnet Genesis Block**: Generate the genesis block for the official MeshChain mainnet.
- **[ ] Public Launch**: Release the official `meshchain-installer` and `meshchain-cli` tools to the public.
- **[ ] Network Monitoring**: Deploy public block explorers and network status dashboards.
- **[ ] Bug Bounty Program**: Launch a bug bounty program to incentivize security researchers to audit the live network.

---

## Phase 2: Privacy Layer Overhaul (Q2-Q3 2026)

The current implementation of ring signatures is flawed and has been disabled. This phase is dedicated to implementing a robust, state-of-the-art privacy solution.

- **[ ] Research & Selection**: Conduct a thorough review of modern blockchain privacy technologies (e.g., RingCT, zk-SNARKs, Mimblewimble) and select the most suitable option for the ESP32 platform's constraints.
- **[ ] Implementation**: Develop and integrate the chosen privacy protocol. This will be a significant engineering effort, likely requiring a hard fork.
- **[ ] Security Audit**: Commission an external, professional security audit specifically focused on the new privacy layer implementation.
- **[ ] Testnet Deployment**: Deploy the new privacy features on a public testnet for extensive community testing.
- **[ ] Mainnet Activation**: Activate the new privacy layer on the mainnet via a scheduled hard fork.

---

## Phase 3: Scalability & Performance (Q4 2026)

As the network grows, performance will become a key concern. This phase focuses on improving the throughput and efficiency of the network.

- **[ ] Dynamic Fees**: Implement a dynamic fee market (similar to Ethereum's EIP-1559) to allow transaction fees to adjust based on network congestion.
- **[ ] Sharding (Research)**: Begin research into layer-2 or sharding solutions to enable parallel transaction processing. This is a long-term research project to determine the feasibility of sharding in a mesh network context.
- **[ ] Optimized Storage**: Investigate more efficient data structures for storing the blockchain on the microSD card to reduce storage footprint and improve read/write speeds.
- **[ ] Fast Sync**: Develop a "fast sync" or "light client" mode that allows new nodes to get up and running quickly without needing to download the entire blockchain history from the genesis block.

---

## Phase 4: Interoperability & Ecosystem (2027)

With a stable, private, and scalable network, the focus will shift to growing the ecosystem and connecting MeshChain to the broader blockchain world.

- **[ ] Mobile Wallet**: Develop a dedicated mobile application (iOS/Android) that can interact with an ESP32 node over Bluetooth, providing a user-friendly interface for managing funds and sending transactions.
- **[ ] Cross-Chain Bridges**: Research and develop trust-minimized bridges to allow MeshCoin to be traded on other blockchains (e.g., as a wrapped token on Ethereum).
- **[ ] Developer SDKs**: Create comprehensive SDKs for popular programming languages (e.g., JavaScript, Python, Go) to make it easier for developers to build applications on top of MeshChain.
- **[ ] Grant Program**: Establish a grant program to fund community-led projects that expand the MeshChain ecosystem.

---

## Beyond 2027: The Vision

Looking further ahead, the vision is for MeshChain to become the de facto standard for decentralized, off-grid value transfer. Future research areas may include:

- **Layer-2 Payment Channels**: Similar to Bitcoin's Lightning Network, to enable near-instant, low-fee transactions.
- **Decentralized Governance**: Implementing a formal on-chain governance system to allow the community to vote on future protocol upgrades.
- **Integration with other IoT Devices**: Expanding beyond the ESP32 to other low-power IoT devices capable of running a full node.
