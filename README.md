# MeshChain
[README.md](https://github.com/user-attachments/files/24257419/README.md)
# MeshChain: Decentralized Blockchain for LoRa Mesh Networks

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status: Beta](https://img.shields.io/badge/Status-Beta-orange.svg)]()

MeshChain is a decentralized blockchain protocol designed to operate independently on LoRa mesh networks, enabling peer-to-peer cryptocurrency transactions without internet connectivity or centralized infrastructure.

## Features

- **Zero Internet Dependency**: Operates entirely on LoRa mesh networks
- **Lightweight**: Runs on resource-constrained ESP32 devices with 240 KB RAM
- **Secure**: Ed25519 cryptography with ring signatures for privacy
- **Fast**: 5-10 second block times, optimized for LoRa networks
- **Decentralized**: DPoP consensus with distributed validator selection
- **User-Friendly**: On-device UI for wallet management and transactions
- **Production-Ready**: Thoroughly tested with 390+ tests (100% pass rate)

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/meshchain.git
cd meshchain

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Running a Node

```bash
# Start a MeshChain node
meshchain --config config.json

# Or use the CLI
python -m meshchain.node.cli --help
```

### Creating a Wallet

```python
from meshchain.wallet import Wallet

# Create a new wallet
wallet = Wallet.create(pin="1234")

# Get wallet address
address = wallet.get_address()

# Send a transaction
tx = wallet.send(recipient="...", amount=100)
```

## Documentation

- **[Whitepaper](docs/WHITEPAPER.md)** - Technical whitepaper and protocol specification
- **[User Guide](docs/USER_GUIDE.md)** - End-user guide for operating MeshChain devices
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Instructions for deploying testnet
- **[UI Guide](docs/UI_GUIDE.md)** - User interface documentation
- **[API Reference](docs/)** - Complete API documentation

## Architecture

MeshChain consists of several key components:

### Core Blockchain (`meshchain/core/`)
- **Block**: Block structure and validation
- **Transaction**: Transaction creation and validation
- **Consensus**: DPoP consensus mechanism
- **Synchronizer**: Blockchain synchronization

### Cryptography (`meshchain/crypto/`)
- Ed25519 signatures
- Ring signatures for sender anonymity
- Stealth addresses for receiver privacy
- Secure key derivation and storage

### Storage (`meshchain/storage/`)
- Lightweight JSON-based storage
- Multi-level caching (RAM + disk)
- Atomic writes for data integrity
- Compression for efficient storage

### Network (`meshchain/network/`)
- Meshtastic serial communication
- Message routing and propagation
- Packet optimization (<237 bytes)
- Peer discovery and reputation

### Wallet (`meshchain/wallet/`)
- On-device wallet management
- PIN-based security
- Seed phrase backup/restore
- Transaction signing

### User Interface (`meshchain/ui/`)
- 128x64 OLED display framework
- Button-based navigation
- Wallet management UI
- Transaction creation UI
- Node status display

### Node (`meshchain/node/`)
- MicroNode core implementation
- Bootstrap system
- Genesis block creation
- CLI interface

## Technology Stack

- **Language**: Python 3.8+
- **Cryptography**: libsodium (via PyNaCl)
- **Storage**: JSON-based (SPIFFS on ESP32)
- **Network**: LoRa mesh (Meshtastic)
- **Consensus**: Delegated Proof of Participation (DPoP)

## Testing

MeshChain includes comprehensive test coverage:

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=meshchain

# Run specific test file
pytest tests/test_crypto.py

# Run tests matching pattern
pytest -k "wallet"
```

**Current Status**: 390+ tests passing (100% pass rate)

## Project Structure

```
meshchain/
├── docs/                  # Documentation
├── meshchain/             # Source code
│   ├── core/             # Blockchain core
│   ├── crypto/           # Cryptography
│   ├── storage/          # Storage layer
│   ├── network/          # Network layer
│   ├── wallet/           # Wallet system
│   ├── ui/               # User interface
│   ├── node/             # Node implementation
│   ├── async/            # Async framework
│   ├── config/           # Configuration
│   ├── testnet/          # Testnet tools
│   └── utils/            # Utilities
├── tests/                # Test suite
├── examples/             # Example code
├── scripts/              # Utility scripts
├── archive/              # Development artifacts
└── README.md             # This file
```

## Development Roadmap

### Phase 1: Foundation (Completed ✅)
- Core blockchain implementation
- DPoP consensus mechanism
- Wallet system with PIN security
- LoRa mesh integration
- On-device UI
- Testnet deployment

### Phase 2: Mainnet Launch (Q1 2026)
- Genesis block creation
- Validator registration
- Community token distribution
- Mainnet launch
- Exchange listings

### Phase 3: Ecosystem (Q2-Q3 2026)
- Smart contracts support
- Decentralized applications
- Cross-chain bridges
- Mobile wallet applications
- Community governance

### Phase 4: Scaling (Q4 2026+)
- Layer 2 scaling solutions
- Sidechain support
- Atomic swaps
- Interoperability with other blockchains

## Security

MeshChain has undergone comprehensive security analysis:

- **Cryptographic Security**: Ed25519 signatures, ChaCha20-Poly1305 encryption
- **Consensus Security**: DPoP prevents 51% attacks with validator slashing
- **Network Security**: Peer verification, message authentication, rate limiting
- **Data Integrity**: Atomic writes, hash verification, chain continuity checks

See [Security Documentation](docs/SECURITY.md) for details.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linting
flake8 meshchain tests

# Format code
black meshchain tests
```

## Tokenomics

**Total Supply**: 21,000,000 tokens (fixed)

**Distribution**:
- Community: 40%
- Validators: 30%
- Development: 20%
- Reserve: 10%

**Block Rewards**:
- Block proposer: 1 token per block
- Validators: 5% of block reward
- Reward halving every 4 years

See [Tokenomics](docs/TOKENOMICS.md) for details.

## Community

- **GitHub**: [MeshChain Repository](https://github.com/yourusername/meshchain)
- **Discord**: [MeshChain Community](https://discord.gg/meshchain)
- **Twitter**: [@MeshChain](https://twitter.com/meshchain)
- **Forum**: [MeshChain Discussions](https://github.com/yourusername/meshchain/discussions)

## License

MeshChain is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Disclaimer

MeshChain is a beta software project. Use at your own risk. The developers are not responsible for any loss of funds or data.

## Acknowledgments

- Meshtastic project for LoRa mesh networking
- libsodium for cryptographic primitives
- Bitcoin and Ethereum for blockchain inspiration
- Monero for privacy features

## Contact

For questions, suggestions, or partnerships, please contact:

- **Email**: hello@meshchain.io
- **GitHub Issues**: [Report a bug](https://github.com/yourusername/meshchain/issues)
- **Discussions**: [Join the conversation](https://github.com/yourusername/meshchain/discussions)

---

**Built with ❤️ for decentralized finance on LoRa mesh networks**
