# MeshChain Network Protocol

This document specifies the MeshChain network protocol for Meshtastic integration.

## Overview

MeshChain uses Meshtastic's message routing to distribute blockchain data. Messages are sent on reserved port numbers and use a compact binary format.

## Message Types

### Port 256: Transaction (PortNum.TEXT_MESSAGE_APP)

Used to broadcast pending transactions to the network.

**Message Format:**
```
Offset  Length  Type        Field
────────────────────────────────────
0       1       uint8       message_type (0x01)
1       110     bytes       transaction_data
────────────────────────────────────
Total:  111 bytes
```

**Transaction Data Format:**
```
Offset  Length  Type        Field
────────────────────────────────────
0       1       uint8       version
1       1       uint8       tx_type
2       2       varint      nonce
4       1       uint8       fee
5       1       uint8       ring_size
6       24      bytes       ring_members (3 x 8-byte IDs)
30      16      bytes       stealth_address
46      8       bytes       amount_encrypted
54      32      bytes       signature
86      2       varint      timestamp
────────────────────────────────────
Total:  ~110 bytes
```

### Port 257: Block Proposal (PortNum.POSITION_APP)

Used by proposers to broadcast new blocks.

**Message Format:**
```
Offset  Length  Type        Field
────────────────────────────────────
0       1       uint8       message_type (0x02)
1       500     bytes       block_data
────────────────────────────────────
Total:  501 bytes
```

**Block Data Format:**
```
Offset  Length  Type        Field
────────────────────────────────────
0       1       uint8       version
1       3       varint      height
4       2       uint16      timestamp
6       16      bytes       previous_hash
22      16      bytes       merkle_root
38      8       uint64      proposer_id
46      1       uint8       validator_count
47      N       bytes       validators (8 bytes each)
47+N    1       uint8       approval_count
48+N    M       bytes       approvals (bit vector)
────────────────────────────────────
Total:  ~500 bytes
```

### Port 258: Block Vote (PortNum.ADMIN_APP)

Used by validators to vote on blocks.

**Message Format:**
```
Offset  Length  Type        Field
────────────────────────────────────
0       1       uint8       message_type (0x03)
1       16      bytes       block_hash
17      1       uint8       vote (0x00=reject, 0x01=approve)
────────────────────────────────────
Total:  18 bytes
```

### Port 259: Sync Request (PortNum.ROUTING_APP)

Used to request blockchain synchronization.

**Message Format:**
```
Offset  Length  Type        Field
────────────────────────────────────
0       1       uint8       message_type (0x04)
1       3       varint      from_height
4       3       varint      to_height
7       1       uint8       sync_type (0x01=headers, 0x02=full)
────────────────────────────────────
Total:  8 bytes
```

### Port 260: Sync Response (PortNum.ROUTING_APP)

Used to respond to synchronization requests.

**Message Format:**
```
Offset  Length  Type        Field
────────────────────────────────────
0       1       uint8       message_type (0x05)
1       3       varint      block_height
4       500     bytes       block_data
────────────────────────────────────
Total:  ~504 bytes
```

## Encoding Specifications

### Variable-Length Integer (VarInt)

Used for efficient encoding of integers.

**Encoding Rules:**
```
Value Range        Bytes    Encoding
0-127              1        0xxxxxxx
128-16,383         2        10xxxxxx xxxxxxxx
16,384-2,097,151   3        110xxxxx xxxxxxxx xxxxxxxx
```

**Examples:**
```
Value: 0
Encoded: 0x00

Value: 127
Encoded: 0x7F

Value: 128
Encoded: 0x80 0x01

Value: 16383
Encoded: 0xFF 0x7F

Value: 16384
Encoded: 0x80 0x80 0x01
```

### Hash Format

All hashes use SHA-256, truncated to 16 bytes (128 bits) for space efficiency.

```python
def hash_data(data: bytes) -> bytes:
    """Hash data and return first 16 bytes."""
    return hashlib.sha256(data).digest()[:16]
```

### Address Format

Addresses are 32-byte Ed25519 public keys, displayed as hex strings.

```
Format: 64 hex characters (32 bytes)
Example: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2
```

## Message Flow

### Transaction Broadcasting

```
User creates transaction
        ↓
Wallet signs transaction
        ↓
Serialize to binary (110 bytes)
        ↓
Send on Port 256 with HopStart=3
        ↓
Meshtastic routes to neighbors
        ↓
Neighbors validate and rebroadcast
        ↓
Transaction reaches all nodes
```

### Block Creation and Voting

```
Proposer creates block
        ↓
Broadcast on Port 257 with HopStart=3
        ↓
Validators receive block
        ↓
Validators verify transactions
        ↓
Validators send vote on Port 258
        ↓
Proposer collects votes
        ↓
If >66% approve: Broadcast finalized block
        ↓
All nodes update blockchain
```

### Blockchain Synchronization

```
New node joins network
        ↓
Send Sync Request on Port 259 (from_height=0)
        ↓
Peers respond with Sync Response on Port 260
        ↓
New node receives blocks one by one
        ↓
New node validates and stores blocks
        ↓
New node catches up to current height
```

## Network Parameters

### Timeouts

| Parameter | Value | Description |
|-----------|-------|-------------|
| Block proposal timeout | 10 seconds | Time to wait for block proposal |
| Vote collection timeout | 2 seconds | Time to wait for validator votes |
| Sync response timeout | 5 seconds | Time to wait for sync response |
| Message retry timeout | 1 second | Time before retrying message |

### Limits

| Parameter | Value | Description |
|-----------|-------|-------------|
| Max validators | 7 | Maximum validators per block |
| Max transactions per block | 5 | Maximum transactions per block |
| Max message size | 237 bytes | Meshtastic payload limit |
| Max block size | 500 bytes | Typical block size |
| Min fee | 1 satoshi | Minimum transaction fee |

### Consensus Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Finality threshold | 66% | Percentage of validators needed for finality |
| Block time | 5-10 seconds | Target block creation time |
| Confirmation time | 10-20 seconds | Time to reach finality |
| Max hop distance | 3 | Maximum hops for validator selection |

## Error Handling

### Invalid Message

If a message cannot be parsed:
1. Log the error
2. Discard the message
3. Continue processing

### Invalid Transaction

If a transaction fails validation:
1. Log the error with transaction hash
2. Do not add to mempool
3. Do not broadcast further

### Invalid Block

If a block fails validation:
1. Log the error with block hash
2. Do not add to blockchain
3. Request resync if multiple failures

### Network Partition

If network is partitioned:
1. Continue processing locally
2. Accept blocks from either partition
3. Resolve on reconnection (longest chain wins)

## Security Considerations

### Message Authentication

All messages are authenticated via:
1. Meshtastic's built-in encryption
2. Cryptographic signatures on transactions
3. Validator signatures on blocks

### Message Ordering

Messages may arrive out of order due to:
1. Multiple hops through mesh
2. Concurrent message propagation
3. Network delays

**Mitigation:**
- Use block heights for ordering
- Use transaction nonces for ordering
- Accept out-of-order messages and reorder

### Message Duplication

Messages may be duplicated due to:
1. Meshtastic's managed flooding
2. Multiple paths through mesh
3. Retransmissions

**Mitigation:**
- Track message hashes
- Ignore duplicate messages
- Use bloom filters for efficiency

## Bandwidth Analysis

### Transaction Broadcasting

```
Transaction size: 110 bytes
Broadcast overhead: 20 bytes (Meshtastic headers)
Total per transaction: 130 bytes

Typical network: 10 transactions per block
Bandwidth per block: 1,300 bytes
Block time: 5-10 seconds
Bandwidth: 130-260 bytes/second = 1-2 kbps
```

### Block Broadcasting

```
Block size: 500 bytes
Broadcast overhead: 20 bytes
Total per block: 520 bytes

Block time: 5-10 seconds
Bandwidth: 52-104 bytes/second = 0.4-0.8 kbps
```

### Consensus Overhead

```
Validators per block: 7
Vote size: 18 bytes
Total votes: 7 × 18 = 126 bytes
Block time: 5-10 seconds
Bandwidth: 12-25 bytes/second = 0.1-0.2 kbps
```

### Total Bandwidth

```
Transactions: 1-2 kbps
Blocks: 0.4-0.8 kbps
Consensus: 0.1-0.2 kbps
─────────────────────────
Total: 1.5-3 kbps average

Meshtastic capacity: 50-500 kbps
Utilization: 0.3-6% (comfortable)
```

## Implementation Checklist

- [ ] Message serialization/deserialization
- [ ] Port number allocation
- [ ] Message validation
- [ ] Error handling
- [ ] Timeout management
- [ ] Bandwidth optimization
- [ ] Testing on real hardware

## References

- Meshtastic Protocol: https://meshtastic.org/docs/developers/protobufs/
- Bitcoin Protocol: https://en.bitcoin.it/wiki/Protocol_documentation
- Monero Protocol: https://www.getmonero.org/resources/research-lab/
