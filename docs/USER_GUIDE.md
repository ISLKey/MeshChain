# MeshChain User Guide

**Version**: 1.0  
**Date**: December 18, 2025  
**Author**: Manus AI

## Table of Contents

1. [Getting Started](#getting-started)
2. [Device Overview](#device-overview)
3. [Basic Navigation](#basic-navigation)
4. [Wallet Management](#wallet-management)
5. [Sending and Receiving Funds](#sending-and-receiving-funds)
6. [Viewing Transactions](#viewing-transactions)
7. [Node Status](#node-status)
8. [Security](#security)
9. [Settings](#settings)
10. [Troubleshooting](#troubleshooting)

---

## Getting Started

### What is MeshChain?

MeshChain is a blockchain network that runs on Meshtastic devices, allowing you to send and receive cryptocurrency without internet connectivity. Your device communicates with other MeshChain nodes via LoRa radio, creating a decentralized mesh network.

### Initial Setup

1. **Power on your device** by connecting it to power or inserting batteries.
2. **Wait for startup** - The device will initialize the blockchain and connect to the network (30-60 seconds).
3. **Set your PIN** - When prompted, enter a 4-6 digit PIN to secure your wallet.
4. **Backup your seed phrase** - Write down your 12-word seed phrase and store it safely. This is critical for wallet recovery.

---

## Device Overview

### Screen

Your device has a small 128x64 pixel OLED display. The screen shows:

- **Top**: Current page or menu name
- **Middle**: Main content (balance, transactions, status, etc.)
- **Bottom**: Status bar with battery, signal, and status information

### Buttons

Your device has three buttons:

- **UP Button**: Navigate up in menus, increase values
- **SELECT Button**: Select menu items, confirm actions
- **DOWN Button**: Navigate down in menus, decrease values

### Status Bar

The status bar at the bottom of the screen shows:

- **Battery**: Battery percentage (0-100%)
- **Signal**: Network signal strength (0-5 bars)
- **Status**: Current status or page name

---

## Basic Navigation

### Navigating Menus

1. **Press UP or DOWN** to move between menu items
2. **Press SELECT** to choose an item
3. **Press BACK** (hold UP for 2 seconds) to go back to the previous menu

### Main Menu

The main menu has four options:

- **Wallet**: Manage your wallet and view balance
- **Transactions**: View transaction history
- **Node Status**: Check blockchain and network status
- **Settings**: Configure device and security settings

---

## Wallet Management

### Viewing Your Balance

1. From the main menu, select **Wallet**
2. Your current balance will be displayed
3. Press DOWN to see your wallet address
4. Press SELECT to copy the address to clipboard

### Creating a New Wallet

1. From the Wallet menu, select **Create Wallet**
2. Enter a name for your wallet (up to 20 characters)
3. Your new wallet will be created with a unique address
4. **IMPORTANT**: Backup your seed phrase immediately

### Backing Up Your Wallet

1. From the Wallet menu, select **Backup**
2. Your 12-word seed phrase will be displayed
3. **Write down all 12 words in order** on a piece of paper
4. Store the paper in a safe place (NOT on your device)
5. Press SELECT to confirm you've written down the phrase

### Restoring a Wallet

1. From the main menu, select **Settings** → **Security**
2. Select **Restore Wallet**
3. Enter your 12-word seed phrase (one word at a time)
4. Your wallet will be restored with all previous transactions

---

## Sending and Receiving Funds

### Receiving Funds

1. From the Wallet menu, select **Receive**
2. Your wallet address will be displayed
3. Share this address with the sender
4. Funds will appear in your wallet once confirmed by the network

### Sending Funds

1. From the Wallet menu, select **Send**
2. **Enter Recipient Address**: Use UP/DOWN to select each character
3. **Enter Amount**: Use UP/DOWN to adjust the amount
4. **Review**: Confirm the recipient and amount
5. **Confirm**: Press SELECT to sign and send the transaction
6. Your transaction will be broadcast to the network

### Transaction Fees

Each transaction includes a small fee (typically 0.001 MeshChain). The fee is automatically calculated and displayed before you confirm.

---

## Viewing Transactions

### Transaction History

1. From the main menu, select **Transactions**
2. A list of recent transactions will be displayed
3. **→** indicates funds sent out
4. **←** indicates funds received
5. Press SELECT to view details of a transaction

### Transaction Details

For each transaction, you can see:

- **Date and Time**: When the transaction occurred
- **Type**: Sent or Received
- **Amount**: How much was sent or received
- **Fee**: Transaction fee paid
- **Status**: Confirmed or Pending
- **Confirmations**: Number of blocks confirming the transaction

---

## Node Status

### Blockchain Status

1. From the main menu, select **Node Status** → **Blockchain**
2. You can see:
   - **Block Height**: Current height of the blockchain
   - **Total Transactions**: Total transactions in the blockchain
   - **Difficulty**: Current mining difficulty
   - **Latest Block Hash**: Hash of the most recent block

### Network Status

1. From the main menu, select **Node Status** → **Network**
2. You can see:
   - **Connected Peers**: Number of nodes you're connected to
   - **Sync Status**: Whether you're synced with the network
   - **Sync Progress**: Percentage of blockchain downloaded
   - **Bandwidth**: Upload and download speeds

### Validators

1. From the main menu, select **Node Status** → **Validators**
2. A list of current network validators will be displayed
3. Press SELECT to view details of a validator

---

## Security

### PIN Protection

Your wallet is protected by a PIN (Personal Identification Number). You must enter your PIN to:

- Unlock your wallet
- Send funds
- View your seed phrase
- Change settings

### Changing Your PIN

1. From the main menu, select **Settings** → **Security**
2. Select **Change PIN**
3. Enter your current PIN
4. Enter your new PIN (4-6 digits)
5. Confirm your new PIN

### Brute-Force Protection

If you enter your PIN incorrectly 3 times, your wallet will be locked for 5 minutes. This prevents someone from guessing your PIN.

### Seed Phrase Security

Your seed phrase is the master key to your wallet. **Never share it with anyone**. Anyone with your seed phrase can access all your funds.

**Important**: 
- Write it down on paper and store it safely
- Do NOT take a screenshot or photo
- Do NOT store it on your device
- Do NOT share it via email or messaging

---

## Settings

### Display Settings

1. From the main menu, select **Settings** → **Display**
2. You can adjust:
   - **Brightness**: 0-100%
   - **Contrast**: 0-100%
   - **Timeout**: Screen auto-off time (seconds)
   - **Invert**: Invert display colors

### Network Settings

1. From the main menu, select **Settings** → **Network**
2. You can adjust:
   - **Frequency**: LoRa frequency (915 MHz, 868 MHz, etc.)
   - **Power**: Transmission power (0-23 dBm)
   - **Bandwidth**: LoRa bandwidth
   - **Spreading Factor**: LoRa spreading factor

### Security Settings

1. From the main menu, select **Settings** → **Security**
2. You can:
   - **Enable/Disable PIN**: Require PIN on startup
   - **Change PIN Length**: 4-6 digits
   - **Set Auto-Lock Timeout**: Lock wallet after inactivity
   - **View Seed Phrase**: Display your 12-word seed phrase

### Node Settings

1. From the main menu, select **Settings** → **Node**
2. You can:
   - **Node Name**: Set a name for your node
   - **Node Role**: Choose Validator or Observer
   - **Stake Amount**: Amount of MeshChain to stake (validators only)

---

## Troubleshooting

### Device Won't Turn On

1. Check that the battery is charged
2. Try connecting to power
3. Wait 30 seconds for the device to boot
4. If still not working, try a hard reset (hold power button for 10 seconds)

### Can't Connect to Network

1. Check that your device is powered on
2. Verify that other MeshChain nodes are nearby (within LoRa range)
3. Check the Network Status page to see connected peers
4. Try moving to a higher location for better signal
5. Check that the LoRa frequency matches other nodes

### Wallet Balance Not Updating

1. Check the Network Status page - ensure you're synced
2. Wait for sync to complete (may take several minutes)
3. Check that you have received confirmations for your transactions
4. Try restarting the device

### Can't Send Funds

1. Verify you have sufficient balance (including fees)
2. Check that you're connected to the network (see Network Status)
3. Verify the recipient address is correct
4. Check that your PIN is correct
5. Wait for network sync to complete

### Forgot Your PIN

Unfortunately, there is no way to recover a forgotten PIN. You will need to:

1. Reset your device to factory settings
2. Restore your wallet using your seed phrase
3. Set a new PIN

**To reset your device**:
1. From the main menu, select **Settings** → **Security**
2. Select **Factory Reset**
3. Confirm the reset (this will erase all data)
4. Follow the setup wizard to restore your wallet

### Lost Your Seed Phrase

If you lost your seed phrase and didn't write it down:

1. Your wallet cannot be recovered if your device is lost or damaged
2. You will need to create a new wallet
3. Any funds in the old wallet will be permanently lost

**Prevention**: Always backup your seed phrase immediately after creating a wallet.

### Device Freezes or Crashes

1. Try restarting the device (power off and on)
2. Check that you have enough storage space
3. Try factory reset if the problem persists
4. Contact support if the issue continues

---

## Getting Help

If you encounter issues not covered in this guide:

1. Check the Troubleshooting section above
2. Review the Technical Documentation
3. Contact MeshChain support

---

## Important Disclaimers

- **No Internet Required**: MeshChain works entirely on LoRa mesh network
- **Decentralized**: No central authority controls your funds
- **Irreversible Transactions**: Once sent, transactions cannot be reversed
- **Backup Your Seed Phrase**: This is your only way to recover your wallet
- **Keep Your PIN Secret**: Anyone with your PIN can access your wallet
- **Limited Range**: LoRa range depends on terrain and obstacles (typically 1-10 km)

---

## Glossary

- **Address**: Your unique wallet identifier (like an account number)
- **Balance**: Total amount of MeshChain in your wallet
- **Block**: A group of transactions confirmed by the network
- **Confirmation**: A block that includes your transaction
- **Fee**: Small amount paid to the network for processing your transaction
- **LoRa**: Long Range radio technology used by Meshtastic
- **Mesh Network**: Network where devices relay messages through each other
- **Node**: A device running MeshChain software
- **PIN**: Personal Identification Number (password)
- **Seed Phrase**: 12 words that can restore your wallet
- **Transaction**: Transfer of funds from one wallet to another
- **Validator**: Node that validates transactions and creates blocks
- **Wallet**: Your account that holds your MeshChain funds

---

**End of User Guide**

For more information, visit the MeshChain documentation at: https://meshchain.io/docs
