> This guide is for node operators and provides information on the day-to-day operations, maintenance, and troubleshooting of a MeshChain node.

# MeshChain Node Operations Guide

## 1. The `meshchain-cli` Command-Line Tool

While the ESP32 node itself runs autonomously, a command-line interface (CLI) tool, `meshchain-cli`, is provided for interacting with a running node (either a local dev node or a remote ESP32 node).

**Installation**:
```bash
pip install meshchain-cli
```

**Connecting to a Node**:
By default, the CLI connects to a local node (`http://127.0.0.1:8545`). To connect to a remote ESP32 node, you must first establish a serial or WiFi connection to it and then use a tool to forward its RPC port.

---

## 2. Common Operations

### Checking Node Status

To get a quick overview of your node's status:

```bash
meshchain-cli status
```

**Output**:
```
{
  "node_id": "...",
  "is_mining": true,
  "block_height": 12345,
  "peer_count": 8,
  "mempool_size": 10
}
```

### Checking Wallet Balance

To check the balance of any address:

```bash
meshchain-cli get-balance <address>
```

**Output**:
```
{
  "pending": "123.45",
  "confirmed": "100.00"
}
```

### Sending Transactions

To send funds from your node's wallet:

```bash
meshchain-cli send <recipient_address> <amount>
```

- **`<recipient_address>`**: The stealth address of the recipient.
- **`<amount>`**: The amount of MeshCoins to send.

---

## 3. Maintenance

MeshChain nodes are designed to be low-maintenance.

### Software Updates

When a new version of the MeshChain node software is released, you can update your ESP32 device by re-running the `meshchain-installer` tool. Your wallet and blockchain data on the microSD card will be preserved.

```bash
meshchain-installer --port /dev/ttyUSB0 --update
```

### Backups

**The most critical piece of data is your 24-word mnemonic seed phrase.** As long as you have this phrase, you can restore your wallet and all your funds on any new device.

The blockchain data itself does not need to be backed up, as it can be re-synced from the network.

### SD Card Health

MicroSD cards have a finite number of write cycles. While MeshChain is designed to minimize unnecessary writes, it is good practice to use a high-quality, endurance-rated microSD card. If you notice performance degradation or errors in the logs related to SD card access, it may be time to replace the card. You can do so by:

1.  Installing a new card.
2.  Re-running the installer.
3.  Restoring your wallet using your mnemonic phrase.
4.  Letting the node re-sync the blockchain from the network.

---

## 4. Troubleshooting

### Node is Not Syncing

1.  **Check LoRa Connection**: Ensure your device has a good LoRa signal and is within range of other Meshtastic nodes.
2.  **Check WiFi Connection**: If you are trying to sync with the global network, ensure the WiFi credentials configured in Meshtastic are correct and that the network has internet access.
3.  **Check Peers**: Use `meshchain-cli get-peers` to see if you are connected to any other nodes. If not, you may need to manually add a peer using `meshchain-cli add-peer`.

### Transactions Stuck in `Pending`

- This is normal if your node is operating in an offline mesh. The transaction will be upgraded to `Confirmed` once your node syncs with the global network.
- If your node *is* connected to the internet and transactions are still pending, it may be because the network fee (`gas`) is too low during a period of high congestion. Future versions will include dynamic fee adjustment.

### Corrupted SD Card

If the node fails to start and the logs indicate a problem with the SD card, it may be corrupted. Follow the steps in the "SD Card Health" section to replace it.

---

## 5. Log Files

The primary source of information for troubleshooting is the node's log output, which can be viewed by connecting to the ESP32's serial port. The logs provide detailed information about:

- Peer connections and disconnections.
- Block creation and validation.
- Transaction processing.
- SD card read/write operations.
- Errors and warnings.
