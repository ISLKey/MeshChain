> This document provides a reference for the JSON-RPC API of a MeshChain node. This API allows developers to build applications that interact with the MeshChain network.

# MeshChain JSON-RPC API Reference

## 1. Overview

The MeshChain API is exposed as a JSON-RPC 2.0 service over HTTP. All requests should be `POST` requests with a JSON body.

**Endpoint**: `http://<node_ip>:8545/`

**Content-Type**: `application/json`

### Request Format

```json
{
  "jsonrpc": "2.0",
  "method": "method_name",
  "params": [param1, param2, ...],
  "id": 1
}
```

### Response Format

```json
{
  "jsonrpc": "2.0",
  "result": "...",
  "id": 1
}
```

---

## 2. Wallet Methods

### `mc_createWallet`

Creates a new wallet.

- **Parameters**: None
- **Returns**: A JSON object containing the new wallet's address and a 24-word mnemonic seed phrase.

**Example Response**:
```json
{
  "address": "mc_1a2b3c...",
  "mnemonic": "word1 word2 ... word24"
}
```

### `mc_getBalance`

Returns the balance of a given address.

- **Parameters**:
    1.  `string` - The address to check.
- **Returns**: A JSON object with the `pending` and `confirmed` balances.

**Example Response**:
```json
{
  "pending": "123.45",
  "confirmed": "100.00"
}
```

### `mc_getNewAddress`

Generates a new stealth address for receiving payments.

- **Parameters**: None
- **Returns**: `string` - A new, unique stealth address.

---

## 3. Transaction Methods

### `mc_sendTransaction`

Creates and broadcasts a new transaction.

- **Parameters**:
    1.  `object` - A transaction object:
        -   `from`: `string` - The sender's address.
        -   `to`: `string` - The recipient's stealth address.
        -   `amount`: `string` - The amount to send.
- **Returns**: `string` - The transaction hash.

### `mc_getTransaction`

Retrieves a transaction by its hash.

- **Parameters**:
    1.  `string` - The transaction hash.
- **Returns**: A JSON object with transaction details, including its status (`Pending` or `Confirmed`).

### `mc_getMempool`

Returns all transactions currently in the mempool (i.e., `Pending` transactions).

- **Parameters**: None
- **Returns**: `array` - A list of transaction objects.

---

## 4. Blockchain Methods

### `mc_getBlockCount`

Returns the current height of the blockchain.

- **Parameters**: None
- **Returns**: `number` - The number of the most recent block.

### `mc_getBlockByNumber`

Retrieves a block by its number.

- **Parameters**:
    1.  `number` - The block number.
    2.  `boolean` - If `true`, returns full transaction objects; if `false`, returns only transaction hashes.
- **Returns**: A block object.

### `mc_getBlockByHash`

Retrieves a block by its hash.

- **Parameters**:
    1.  `string` - The block hash.
- **Returns**: A block object.

---

## 5. Network Methods

### `mc_getPeerCount`

Returns the number of connected peers.

- **Parameters**: None
- **Returns**: `number` - The number of peers.

### `mc_getPeers`

Returns information about connected peers.

- **Parameters**: None
- **Returns**: `array` - A list of peer objects, including their IP addresses and block heights.

### `mc_addPeer`

Manually adds a peer to the connection list.

- **Parameters**:
    1.  `string` - The IP address and port of the peer (e.g., `192.168.1.100:8545`).
- **Returns**: `boolean` - `true` if the peer was added successfully.

---

## 6. Node Status

### `mc_getStatus`

Returns the current status of the node.

- **Parameters**: None
- **Returns**: A JSON object with status information.

**Example Response**:
```json
{
  "node_id": "...",
  "is_mining": true,
  "block_height": 12345,
  "peer_count": 8,
  "mempool_size": 10
}
```
