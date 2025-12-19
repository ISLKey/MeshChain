> This guide provides a practical, step-by-step walkthrough for developers looking to build applications on the MeshChain network. It covers setting up a development environment, creating a wallet, and sending your first transaction.

# MeshChain Implementation Guide

## 1. Setting Up Your Development Environment

Before you can interact with the MeshChain network, you'll need to have a node running.

### Step 1: Install MeshChain

The MeshChain software is distributed as a Python package. You can install it using `pip`.

```bash
# It is recommended to use a virtual environment
python3 -m venv meshchain-env
source meshchain-env/bin/activate

pip install meshchain
```

### Step 2: Run a Local Node

For development, you can run a node in `--dev` mode. This creates a local, single-node blockchain that produces blocks every 10 seconds, making development much faster.

```bash
meshchain-cli run --dev
```

This command will start a local node and expose the JSON-RPC API at `http://127.0.0.1:8545`.

---

## 2. Interacting with the Node: Your First Wallet

We will use `curl` to interact with the node's JSON-RPC API. 

### Step 1: Create a Wallet

Let's create a new wallet to hold our funds.

```bash
curl -X POST -H "Content-Type: application/json" --data '{ "jsonrpc": "2.0", "method": "mc_createWallet", "params": [], "id": 1 }' http://127.0.0.1:8545
```

The response will contain your new address and your secret mnemonic phrase. **Save the mnemonic in a safe place!**

```json
{
  "jsonrpc": "2.0",
  "result": {
    "address": "mc_1...",
    "mnemonic": "apple banana cherry ..."
  },
  "id": 1
}
```

### Step 2: Check Your Balance

In `--dev` mode, new wallets are automatically funded with test coins. Let's check the balance.

```bash
curl -X POST -H "Content-Type: application/json" --data '{ "jsonrpc": "2.0", "method": "mc_getBalance", "params": ["mc_1..."], "id": 2 }' http://127.0.0.1:8545
```

**Response**:
```json
{
  "jsonrpc": "2.0",
  "result": {
    "pending": "1000.00",
    "confirmed": "1000.00"
  },
  "id": 2
}
```

---

## 3. Sending a Transaction

Now, let's send some coins. To do this, we need a recipient. We'll create a second wallet to send funds to.

### Step 1: Create a Recipient Wallet

Run the `mc_createWallet` command again to get a second address.

```bash
# Request
curl -X POST -H "Content-Type: application/json" --data '{ "jsonrpc": "2.0", "method": "mc_createWallet", "params": [], "id": 3 }' http://127.0.0.1:8545

# Response (save this new address)
# { "result": { "address": "mc_2...", ... } }
```

### Step 2: Send the Transaction

Now, we'll send 10 coins from our first wallet (`mc_1...`) to our second wallet (`mc_2...`).

```bash
curl -X POST -H "Content-Type: application/json" --data '
{
  "jsonrpc": "2.0",
  "method": "mc_sendTransaction",
  "params": [{
    "from": "mc_1...",
    "to": "mc_2...",
    "amount": "10.0"
  }],
  "id": 4
}' http://127.0.0.1:8545
```

The response will be the transaction hash.

```json
{
  "jsonrpc": "2.0",
  "result": "0x123abc...",
  "id": 4
}
```

### Step 3: Check the Balances

If you check the balances of both accounts, you will see the changes reflected.

- The sender's balance will be down by 10.
- The recipient's balance will be up by 10.

Because we are in `--dev` mode, the transaction will be in the `Confirmed` state almost immediately.

---

## 4. A Simple Python Application

Here is a simple Python script that uses the `requests` library to interact with the MeshChain node.

```python
import requests
import json

# --- Configuration ---
NODE_URL = "http://127.0.0.1:8545"
HEADERS = {'Content-Type': 'application/json'}

# --- Helper Function ---
def rpc_call(method, params):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }
    response = requests.post(NODE_URL, headers=HEADERS, data=json.dumps(payload))
    return response.json()['result']

# --- Main Logic ---
if __name__ == "__main__":
    # 1. Get Node Status
    status = rpc_call("mc_getStatus", [])
    print(f"Connected to node at block height: {status['block_height']}\n")

    # 2. Create two wallets
    print("Creating wallets...")
    wallet1 = rpc_call("mc_createWallet", [])
    wallet2 = rpc_call("mc_createWallet", [])
    print(f"  Wallet 1 Address: {wallet1['address']}")
    print(f"  Wallet 2 Address: {wallet2['address']}\n")

    # 3. Check initial balance of Wallet 1
    balance1_before = rpc_call("mc_getBalance", [wallet1['address']])
    print(f"Wallet 1 starting balance: {balance1_before['confirmed']} MC\n")

    # 4. Send 25 MC from Wallet 1 to Wallet 2
    print("Sending 25 MC from Wallet 1 to Wallet 2...")
    tx_params = {
        "from": wallet1['address'],
        "to": wallet2['address'],
        "amount": "25.0"
    }
    tx_hash = rpc_call("mc_sendTransaction", [tx_params])
    print(f"  Transaction sent! Hash: {tx_hash}\n")

    # 5. Check final balances
    # Note: In --dev mode, blocks are fast. In production, you'd need to wait.
    balance1_after = rpc_call("mc_getBalance", [wallet1['address']])
    balance2_after = rpc_call("mc_getBalance", [wallet2['address']])

    print(f"Wallet 1 final balance: {balance1_after['confirmed']} MC")
    print(f"Wallet 2 final balance: {balance2_after['confirmed']} MC")

```

This script demonstrates the basic flow of creating wallets, checking balances, and sending transactions programmatically. You can use this as a starting point for your own applications.
