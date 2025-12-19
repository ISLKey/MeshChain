#!/usr/bin/env python3
"""
Example 1: Creating a Basic Wallet

This example shows how to:
1. Create a keypair for signing transactions
2. Create a stealth address for receiving payments
3. Display wallet information
"""

import sys
sys.path.insert(0, '..')

from meshchain.crypto import KeyPair, StealthAddress


def main():
    print("=" * 60)
    print("MeshChain Example 1: Creating a Basic Wallet")
    print("=" * 60)
    
    # Step 1: Create a keypair for signing
    print("\n1. Generating signing keypair...")
    signing_key = KeyPair()
    print(f"   Private key: {signing_key.private_key.hex()[:32]}...")
    print(f"   Public key: {signing_key.public_key.hex()[:32]}...")
    print(f"   Address: {signing_key.address[:16]}...")
    
    # Step 2: Create a stealth address for receiving
    print("\n2. Generating stealth address...")
    stealth = StealthAddress()
    stealth_addr = stealth.get_address()
    print(f"   Spend key: {stealth.spend_key.hex()[:32]}...")
    print(f"   View key: {stealth.view_key.hex()[:32]}...")
    print(f"   Stealth address: {stealth_addr.hex()}")
    
    # Step 3: Display wallet summary
    print("\n3. Wallet Summary:")
    print(f"   Signing address: {signing_key.address[:32]}...")
    print(f"   Stealth address: {stealth_addr.hex()}")
    print(f"   Type: Basic Wallet (no balance tracking)")
    
    # Step 4: Test signing
    print("\n4. Testing transaction signing...")
    message = b"Hello from MeshChain!"
    signature = signing_key.sign(message)
    print(f"   Message: {message.decode()}")
    print(f"   Signature: {signature.hex()[:32]}...")
    
    # Step 5: Verify signature
    print("\n5. Verifying signature...")
    is_valid = KeyPair.verify(signing_key.public_key, message, signature)
    print(f"   Signature valid: {is_valid}")
    
    print("\n" + "=" * 60)
    print("Wallet creation successful!")
    print("=" * 60)


if __name__ == "__main__":
    main()
