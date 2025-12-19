> # MeshChain Testnet Setup Guide
> **Date**: December 19, 2025
> **Author**: Manus AI
> **Status**: Guide

---

## 1. Introduction

This guide provides step-by-step instructions for setting up a local MeshChain testnet using two or more TTGO T-Display ESP32 devices. The testnet will allow you to experiment with the MeshChain protocol, create wallets, send transactions, and watch the blockchain grow from the genesis block.

## 2. Prerequisites

### 2.1 Hardware

- 2x TTGO T-Display ESP32 devices
- 2x Micro USB cables

### 2.2 Software

- [Arduino IDE](https://www.arduino.cc/en/software)
- [ESP32 Board Support for Arduino](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html)
- [TFT_eSPI Library](https://github.com/Bodmer/TFT_eSPI)

## 3. Software Setup

1.  **Install the Arduino IDE**: Download and install the Arduino IDE for your operating system.
2.  **Install ESP32 Board Support**: Follow the instructions to add ESP32 board support to your Arduino IDE.
3.  **Install TFT_eSPI Library**: Download the TFT_eSPI library and install it in your Arduino IDE.

## 4. Flashing the ESP32s

For each of your TTGO T-Display devices, you will need to upload the `meshchain_esp32.ino` sketch.

1.  **Open the Sketch**: Open the `meshchain_esp32.ino` sketch in the Arduino IDE.
2.  **Select the Board**: In the Arduino IDE, go to `Tools > Board` and select `TTGO LoRa32-OLED V1`.
3.  **Select the Port**: Connect your TTGO T-Display to your computer and select the correct port under `Tools > Port`.
4.  **Upload the Sketch**: Click the `Upload` button to compile and upload the sketch to the device.

Repeat this process for each of your ESP32 devices.

## 5. Starting the Testnet

Once all your devices have been flashed, you can start the testnet:

1.  **Power On**: Power on each of your ESP32 devices. You should see the MeshChain splash screen on the display.
2.  **Network Formation**: The devices will automatically begin to search for each other and form a mesh network. The display will show the number of peers each node is connected to.

## 6. The Genesis Block

The first block of the blockchain, known as the **genesis block**, is automatically created when the first node in the network starts up. All subsequent blocks will be built on top of this genesis block.

## 7. Performing Transactions

To send and receive transactions, you will need to use the `wallet_ui.ino` and `send_transaction.ino` sketches.

### 7.1 Viewing Your Wallet

1.  Upload the `wallet_ui.ino` sketch to one of your devices.
2.  The display will show your wallet balance and public address.

### 7.2 Sending a Transaction

1.  Upload the `send_transaction.ino` sketch to another device.
2.  Modify the `recipientAddress` and `amount` variables in the sketch to specify the recipient and amount for your transaction.
3.  Upload the sketch. The device will send the transaction to the network, and the display will show the result.

## 8. Building the Blockchain

As you and other users on the testnet send transactions, the validator nodes will group them into blocks and add them to the blockchain. You can observe the block height increasing on the main display of the `meshchain_esp32.ino` sketch.

## 9. Troubleshooting

- **Device not recognized**: Make sure you have the correct drivers installed for your ESP32 device.
- **Sketch fails to compile**: Ensure you have installed all the required libraries correctly.
- **Nodes not connecting**: Check that the LoRa settings (frequency, etc.) are the same on all devices.
