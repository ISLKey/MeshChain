# Phase 1 Implementation Guide: Core Blockchain

This guide walks you through implementing Phase 1 of MeshChain—the core blockchain components.

## Overview

Phase 1 consists of four main components:

1. **Cryptography Module** (`crypto.py`) - Signing, ring signatures, stealth addresses
2. **UTXO Model** (`utxo.py`) - Transaction outputs and balance management
3. **Storage Layer** (`storage.py`) - Persistent blockchain data
4. **Transaction & Block** (already complete) - Data structures

## Prerequisites

Before starting, ensure you have:

- Python 3.11+
- Virtual environment set up
- Required dependencies installed

```bash
cd meshchain
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Component 1: Cryptography Module

### What It Does

The cryptography module provides:
- **KeyPair**: Ed25519 key generation and signing
- **StealthAddress**: Privacy for receivers
- **RingSignature**: Anonymity for senders
- **AmountEncryption**: Hiding transaction amounts

### Key Classes

#### KeyPair

```python
from meshchain.crypto import KeyPair

# Generate a new keypair
keypair = KeyPair()

# Get the address
address = keypair.address

# Sign a message
message = b"Hello, MeshChain!"
signature = keypair.sign(message)

# Verify a signature
is_valid = KeyPair.verify(keypair.public_key, message, signature)
```

#### StealthAddress

```python
from meshchain.crypto import StealthAddress

# Generate a new stealth address
stealth = StealthAddress()

# Get the address (16 bytes)
address = stealth.get_address()

# Check if an output belongs to this address
can_spend = stealth.can_spend(transaction_key, ephemeral_public)
```

#### RingSignature

```python
from meshchain.crypto import RingSignature

# Create a ring signature
ring_members = [pub_key1, pub_key2, pub_key3, pub_key4]
signature = RingSignature.create_ring(
    message=b"transaction data",
    ring_members=ring_members,
    signer_index=2,  # Which key actually signed
    private_key=my_private_key
)

# Verify the ring signature
is_valid = RingSignature.verify_ring(message, ring_members, signature)
```

#### AmountEncryption

```python
from meshchain.crypto import AmountEncryption

# Encrypt an amount
amount = 12345  # satoshis
encrypted, ephemeral = AmountEncryption.encrypt_amount(
    amount,
    recipient_public_key
)

# Decrypt (only recipient can do this)
decrypted = AmountEncryption.decrypt_amount(
    encrypted,
    ephemeral,
    recipient_private_key
)
```

### Testing the Cryptography Module

```bash
# Run the built-in test
python3 meshchain/crypto.py
```

Expected output:
```
MeshChain Cryptography Module
==================================================
1. Testing KeyPair...
   Generated keypair: KeyPair(address=...)
   Signed message, signature length: 64 bytes
   Signature valid: True
2. Testing StealthAddress...
   Generated stealth address: StealthAddress(...)
3. Testing RingSignature...
   Created ring signature: 64 bytes
   Ring signature valid: True
4. Testing AmountEncryption...
   Encrypted amount: 24 bytes
   Ephemeral public key: 32 bytes
==================================================
All cryptographic operations working!
```

## Component 2: UTXO Model

### What It Does

The UTXO model manages:
- **UTXO**: Individual unspent outputs
- **UTXOSet**: Collection of all UTXOs
- **TransactionValidator**: Validates transactions

### Key Classes

#### UTXO

```python
from meshchain.utxo import UTXO

# Create a UTXO
utxo = UTXO(
    utxo_id=b'\x01' * 16,  # Unique identifier
    amount=1000,            # In satoshis
    stealth_address=b'\x02' * 16,  # Recipient
    block_height=1          # When created
)

# Serialize for storage
data = utxo.serialize()

# Deserialize from storage
utxo = UTXO.deserialize(data)
```

#### UTXOSet

```python
from meshchain.utxo import UTXOSet

# Create UTXO set
utxo_set = UTXOSet()

# Add UTXOs
utxo_set.add_utxo(utxo1)
utxo_set.add_utxo(utxo2)

# Check balance
balance = utxo_set.get_balance(stealth_address)

# Get unspent UTXOs for an address
unspent = utxo_set.get_unspent_utxos(stealth_address)

# Spend a UTXO
utxo_set.spend_utxo(utxo_id)

# Check if UTXO is unspent
is_unspent = utxo_set.is_unspent(utxo_id)
```

#### TransactionValidator

```python
from meshchain.utxo import TransactionValidator
from meshchain.transaction import Transaction

# Create validator
validator = TransactionValidator(utxo_set)

# Validate a transaction
is_valid, error_msg = validator.validate_transaction(tx)
if is_valid:
    print("Transaction is valid!")
else:
    print(f"Validation error: {error_msg}")

# Check for double-spending
no_double_spend = validator.check_double_spend(tx)

# Estimate appropriate fee
fee = validator.estimate_fee(tx_size=110)
```

### Testing the UTXO Model

```bash
python3 meshchain/utxo.py
```

Expected output:
```
MeshChain UTXO Model
==================================================
1. Creating UTXO set...
   Added 2 UTXOs
   UTXO set size: 2
2. Checking balance...
   Balance for address: 3000 satoshis
3. Spending UTXO...
   Spent UTXO
   Unspent count: 1
   New balance: 2000 satoshis
4. Testing serialization...
   Serialized UTXO set: 98 bytes
   Deserialized UTXO set size: 2
==================================================
UTXO model working correctly!
```

## Component 3: Storage Layer

### What It Does

The storage layer provides:
- **BlockchainStorage**: SQLite-based persistent storage
- Block and transaction storage
- UTXO management
- Node state persistence

### Key Methods

```python
from meshchain.storage import BlockchainStorage

# Create storage
storage = BlockchainStorage("meshchain.db")

# Add a block
storage.add_block(block)

# Get a block
block = storage.get_block(height=1)

# Add a transaction
storage.add_transaction(tx, block_height=1, tx_index=0)

# Get a transaction
tx = storage.get_transaction(tx_hash)

# Add a UTXO
storage.add_utxo(utxo)

# Get balance
balance = storage.get_balance(stealth_address)

# Get unspent UTXOs
utxos = storage.get_unspent_utxos(stealth_address)

# Spend a UTXO
storage.spend_utxo(utxo_id)

# Node state
storage.set_state("last_block_height", "100")
height = storage.get_state("last_block_height")

# Get statistics
stats = storage.get_statistics()
print(f"Blocks: {stats['blocks']}")
print(f"Transactions: {stats['transactions']}")
print(f"UTXOs: {stats['utxos']}")
print(f"Total value: {stats['total_value']}")

# Close database
storage.close()
```

### Testing the Storage Layer

```bash
python3 meshchain/storage.py
```

Expected output:
```
MeshChain Storage Module
==================================================
1. Creating storage...
   Storage initialized
2. Adding UTXO...
   UTXO added
3. Checking balance...
   Balance: 1000 satoshis
4. Setting node state...
   State saved
5. Getting node state...
   Last block height: 1
   Network ID: meshchain-testnet
6. Getting statistics...
   Blocks: 0
   Transactions: 0
   UTXOs: 1
   Total value: 1000 satoshis
==================================================
Storage module working correctly!
```

## Putting It All Together

### Example: Creating and Validating a Transaction

```python
from meshchain.crypto import KeyPair, RingSignature, AmountEncryption
from meshchain.transaction import Transaction, TransactionType
from meshchain.utxo import TransactionValidator, UTXOSet
from meshchain.storage import BlockchainStorage

# 1. Create keypairs
sender = KeyPair()
receiver = KeyPair()

# 2. Create UTXOs for sender
utxo_set = UTXOSet()
utxo = UTXO(
    utxo_id=b'\x01' * 16,
    amount=1000,
    stealth_address=sender.public_key[:16],  # Simplified
    block_height=1
)
utxo_set.add_utxo(utxo)

# 3. Create a transaction
tx = Transaction(
    version=1,
    tx_type=TransactionType.TRANSFER,
    nonce=1,
    fee=5,
    ring_size=4,
    ring_members=[sender.public_key[:8]] * 4,  # Simplified
    stealth_address=receiver.public_key[:16],  # Simplified
    amount_encrypted=b'\x00' * 8,
    signature=b'\x00' * 32,
    timestamp=1
)

# 4. Validate transaction
validator = TransactionValidator(utxo_set)
is_valid, error = validator.validate_transaction(tx)

if is_valid:
    print("Transaction is valid!")
else:
    print(f"Transaction invalid: {error}")

# 5. Store in database
storage = BlockchainStorage("meshchain.db")
storage.add_utxo(utxo)
storage.add_transaction(tx, block_height=1, tx_index=0)
storage.close()
```

## Common Patterns

### Pattern 1: Creating a Wallet

```python
from meshchain.crypto import KeyPair, StealthAddress

class Wallet:
    def __init__(self):
        self.signing_key = KeyPair()
        self.stealth_address = StealthAddress()
    
    def get_address(self):
        return self.stealth_address.get_address()
    
    def sign_transaction(self, tx_data):
        return self.signing_key.sign(tx_data)
```

### Pattern 2: Checking Balance

```python
from meshchain.storage import BlockchainStorage

def check_balance(db_path, stealth_address):
    storage = BlockchainStorage(db_path)
    balance = storage.get_balance(stealth_address)
    storage.close()
    return balance
```

### Pattern 3: Creating a Transaction

```python
from meshchain.transaction import Transaction, TransactionType
from meshchain.crypto import RingSignature, AmountEncryption

def create_transaction(sender_key, receiver_address, amount, fee):
    # Encrypt amount
    encrypted, ephemeral = AmountEncryption.encrypt_amount(
        amount,
        receiver_address
    )
    
    # Create ring signature
    ring_members = [...]  # Get from network
    signature = RingSignature.create_ring(
        message=b"transaction",
        ring_members=ring_members,
        signer_index=0,
        private_key=sender_key.private_key
    )
    
    # Create transaction
    tx = Transaction(
        version=1,
        tx_type=TransactionType.TRANSFER,
        nonce=1,
        fee=fee,
        ring_size=len(ring_members),
        ring_members=ring_members,
        stealth_address=receiver_address,
        amount_encrypted=encrypted,
        signature=signature,
        timestamp=0
    )
    
    return tx
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'nacl'"

**Solution:** Install dependencies
```bash
pip install PyNaCl pycryptodome
```

### Issue: "ValueError: Private key must be 32 bytes"

**Solution:** Ensure you're using 32-byte keys
```python
# Wrong
key = b'\x01' * 16  # Only 16 bytes

# Correct
key = b'\x01' * 32  # 32 bytes
```

### Issue: "UTXO already exists"

**Solution:** Check if UTXO ID is unique
```python
# Make sure UTXO IDs are unique
utxo_id = hashlib.sha256(data).digest()[:16]
```

## Next Steps

After completing Phase 1, you'll be ready for:

1. **Phase 2**: Implement the consensus mechanism (DPoP)
2. **Phase 3**: Integrate with Meshtastic network
3. **Phase 4**: Testing and optimization
4. **Phase 5**: Create wallets and tools

## Resources

- [Python Cryptography](https://cryptography.io/)
- [PyNaCl Documentation](https://pynacl.readthedocs.io/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [MeshChain Architecture](./ARCHITECTURE.md)
- [MeshChain Protocol](./PROTOCOL.md)

## Questions?

If you get stuck:

1. Check the example code in each module
2. Run the built-in tests
3. Read the docstrings
4. Open an issue on GitHub
5. Ask in GitHub Discussions

Good luck building MeshChain!
