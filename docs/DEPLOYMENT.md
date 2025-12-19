> This guide provides instructions for deploying a MeshChain node on an ESP32 device, turning it into a fully functional part of the mesh network.

# MeshChain ESP32 Deployment Guide

## 1. Hardware Requirements

To run a MeshChain node, you will need the following hardware:

- **ESP32 Device**: A compatible ESP32 board. The following are well-tested:
    - LILYGO T-Beam V1.1 (recommended for its integrated GPS and LoRa module)
    - Heltec WiFi LoRa 32 (V2)
- **MicroSD Card**: A microSD card with at least **8 GB** of storage. A Class 10 or faster card is recommended for performance.
- **MicroSD Card Reader**: A module to connect the microSD card to the ESP32 (if not already built-in).
- **LoRa Antenna**: An antenna appropriate for your region's LoRa frequency (e.g., 915 MHz for North America, 868 MHz for Europe).
- **Power Supply**: A reliable power source, such as a USB power bank or a permanent wall adapter.

---

## 2. Software Prerequisites

### Step 1: Install Meshtastic Firmware

MeshChain runs on top of the Meshtastic firmware, which provides the underlying LoRa mesh networking capabilities.

1.  **Download the Meshtastic Flasher**: Go to the [Meshtastic releases page](https://github.com/meshtastic/firmware/releases) and download the flasher tool for your operating system.
2.  **Connect Your ESP32**: Connect your ESP32 device to your computer via USB.
3.  **Flash the Firmware**: Run the Meshtastic flasher and select the correct serial port for your device. Choose the latest stable firmware version and flash it to the board.
4.  **Initial Configuration**: Use the Meshtastic client app (available for web, Android, and iOS) to connect to your device and configure its basic settings, such as the LoRa channel and region.

### Step 2: Prepare the MicroSD Card

1.  **Format the Card**: Format your microSD card to **FAT32**. This is the most compatible filesystem for ESP32.
2.  **Insert the Card**: Insert the formatted microSD card into the reader connected to your ESP32.

---

## 3. Installing the MeshChain Software

The MeshChain node software is installed using a Python-based installer that runs on your computer.

### Step 1: Install the Installer Tool

On your computer, open a terminal and install the `meshchain-installer` package from `pip`.

```bash
# Ensure you have Python 3 and pip installed
pip install meshchain-installer
```

### Step 2: Run the Installer

With your ESP32 connected to your computer, run the installer.

```bash
meshchain-installer --port /dev/ttyUSB0
```

- **`--port`**: Replace `/dev/ttyUSB0` with the correct serial port for your ESP32 device.

The installer will automatically:
1.  Detect the ESP32 and the microSD card.
2.  Install the latest version of the MeshChain node software onto the ESP32.
3.  Create a default configuration file.
4.  Generate a new wallet for the node.

### Step 3: Initial Configuration

After the installation, the installer will display the node's new address and mnemonic seed phrase. **Store this mnemonic phrase in a secure, offline location. It is the only way to recover your wallet.**

You can connect to the device's serial console (using a tool like `minicom` or the Arduino IDE's Serial Monitor) to view the node's startup logs and confirm it is running correctly.

---

## 4. Starting the Node

Once the installation is complete, the MeshChain node will start automatically whenever the ESP32 is powered on. No further action is needed.

The node will:
1.  Initialize the LoRa radio and connect to the Meshtastic network.
2.  Load the blockchain from the microSD card.
3.  Begin syncing with any peers it discovers on the mesh.
4.  If it has an internet connection (via WiFi configured in Meshtastic), it will attempt to connect to the global network to sync the blockchain.

---

## 5. Verifying the Installation

You can verify that your node is running correctly by:

- **Checking the Device Logs**: Connect to the serial console to see real-time logs of the node's activity, including peer connections, block syncing, and transaction processing.
- **Using a Block Explorer**: If your node is connected to the internet, you can look up its address in a public MeshChain block explorer to see its balance and transaction history.
