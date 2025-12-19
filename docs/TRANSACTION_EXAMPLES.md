> # MeshChain Transaction Examples and Testing Guide
> **Date**: December 19, 2025
> **Author**: Manus AI
> **Status**: Guide

---

## 1. Introduction

This guide provides practical examples of how to create and verify transactions on the MeshChain testnet. It is designed to be used in conjunction with the `TESTNET_SETUP_GUIDE.md`.

## 2. Example 1: Sending a Simple Transaction

This example demonstrates a basic transfer of funds between two users.

### 2.1 Scenario

- **Alice** wants to send **10 MC** to **Bob**.
- Alice's address: `mc_alice123`
- Bob's address: `mc_bob456`

### 2.2 Steps

1.  **Alice's Device**: Upload the `send_transaction.ino` sketch to Alice's TTGO T-Display.
2.  **Modify the Sketch**: In the `setup()` function, set the recipient and amount:
    ```cpp
    String recipientAddress = "mc_bob456";
    float amount = 10.0;
    ```
3.  **Upload and Send**: Upload the modified sketch to Alice's device. The transaction will be broadcast to the network.
4.  **Bob's Device**: Upload the `wallet_ui.ino` sketch to Bob's device. After the next block is produced, Bob's balance should increase by 10 MC.

## 3. Example 2: Becoming a Validator (Bonding)

This example shows how a user can become a validator by bonding (staking) their funds.

### 3.1 Scenario

- **Charlie** wants to become a validator and is willing to bond **1000 MC**.
- Charlie's address: `mc_charlie789`

### 3.2 Steps

1.  **Charlie's Device**: You will need a modified version of the `send_transaction.ino` sketch that can create a `BOND` transaction.
    ```cpp
    // In a real implementation, the MeshChain library would have a
    // function like this:
    meshChainNode.sendBondTransaction(1000.0);
    ```
2.  **Verify Validator Status**: After the bond transaction is confirmed, Charlie will be added to the list of active validators. This can be verified through a network status API (to be implemented).

## 4. Example 3: Testing Double-Spend Prevention

This example demonstrates how the network prevents a user from spending the same funds twice.

### 4.1 Scenario

- **Eve** has **5 MC** and attempts to send 5 MC to both **Alice** and **Bob**.

### 4.2 Steps

1.  **First Transaction**: Eve sends 5 MC to Alice. This transaction is broadcast and enters the mempool.
2.  **Second Transaction**: Eve immediately tries to send the same 5 MC to Bob.
3.  **Mempool Rejection**: The second transaction will be rejected by the mempool because the UTXOs it is trying to spend are already locked by the first transaction.
4.  **Result**: Alice will receive the 5 MC, and Bob will receive nothing. Eve's double-spend attempt will fail.

## 5. Conclusion

These examples provide a basic framework for testing the core functionality of the MeshChain testnet. As the software evolves, more complex scenarios can be tested, including network partitions, validator slashing, and governance proposals forking, and reorgs.
