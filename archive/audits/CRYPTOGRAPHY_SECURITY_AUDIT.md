# Cryptography & Hardware Security Audit

**Date**: December 18, 2025  
**Scope**: Cryptographic implementation, hardware-level attacks, and embedded device security  
**Focus**: MeshChain on ESP32 with Meshtastic LoRa integration

---

## EXECUTIVE SUMMARY

The cryptographic implementation uses solid primitives (Ed25519, ECDH, SHA256) but has **critical vulnerabilities** in:
1. **Side-channel attacks** - No protection against timing/power analysis
2. **Hardware constraints** - ESP32 has no secure enclave
3. **Key management** - Keys stored in plaintext RAM
4. **Random number generation** - May not be cryptographically secure on ESP32
5. **Replay protection** - Missing nonce/timestamp validation
6. **Ring signature implementation** - Non-standard, potentially flawed
7. **Stealth address ECDH** - Simplified implementation, not standard ECDH

---

## PART 1: CRYPTOGRAPHIC PRIMITIVES ANALYSIS

### 1.1 Ed25519 Signature Scheme

**Status**: ✅ **GOOD** - Uses libsodium (NaCl)

**Implementation**:
```python
from nacl.signing import SigningKey, VerifyKey

# Key generation
signing_key = SigningKey.generate()  # 32 bytes
verify_key = signing_key.verify_key  # 32 bytes

# Signing
signature = signing_key.sign(message).signature  # 64 bytes

# Verification
verify_key.verify(message, signature)
```

**Strengths**:
- ✅ Uses libsodium (audited, production-grade library)
- ✅ Ed25519 is modern, secure curve
- ✅ Deterministic signatures (no random nonce)
- ✅ Immune to timing attacks (constant-time operations)
- ✅ Proper key validation in verify()

**Weaknesses**:
- ⚠️ No protection against side-channel attacks on ESP32
- ⚠️ Keys in plaintext RAM during operation
- ⚠️ No key rotation mechanism
- ⚠️ No key expiration

**Risk Level**: 🟡 **MEDIUM** (for embedded device)

---

### 1.2 Stealth Address Implementation (ECDH)

**Status**: 🔴 **CRITICAL** - Non-standard, potentially broken

**Current Implementation**:
```python
# Simplified ECDH (NOT standard ECDH)
shared_secret = hashlib.sha256(ephemeral_private + self.spend_public).digest()
one_time_key = hashlib.sha256(shared_secret + self.view_public).digest()
output_key = hashlib.sha256(one_time_key).digest()[:16]
```

**Problems**:

1. **Not Actual ECDH**: 
   - Real ECDH: `shared_secret = ephemeral_private * spend_public` (scalar multiplication)
   - Current: `hash(ephemeral_private || spend_public)` (concatenation)
   - This is cryptographically unsound

2. **Key Derivation Issues**:
   - Using SHA256 for key derivation (not HKDF)
   - No domain separation between different uses
   - Truncating to 16 bytes (128 bits) for output_key
   - Multiple hash layers without clear purpose

3. **Receiver Privacy Broken**:
   - Sender generates ephemeral_public
   - Receiver can't verify without knowing ephemeral_private
   - Current implementation doesn't match stealth address protocol

4. **No Key Derivation Standard**:
   - Should use HKDF (HMAC-based KDF)
   - Should use standard domain separation
   - Should follow Monero stealth address protocol

**Attack Vector**: 🔴 **CRITICAL**
- Attacker can potentially derive one-time keys
- Receiver privacy not guaranteed
- Transactions may be linkable

**Risk Level**: 🔴 **CRITICAL**

---

### 1.3 Ring Signature Implementation

**Status**: 🔴 **CRITICAL** - Non-standard, likely broken

**Current Implementation**:
```python
# For signer
challenge = hashlib.sha256(commitment + bytes([i])).digest()
response = xor(nonce, xor(challenge, private_key))

# For non-signers
challenge = random(32)
response = random(32)
```

**Problems**:

1. **Not a Real Ring Signature**:
   - Real ring signatures: Schnorr-based with commitment chains
   - Current: Random challenges/responses for non-signers
   - No cryptographic link between ring members

2. **Signer Identification**:
   - Response computation is deterministic for signer
   - Response is random for non-signers
   - Attacker can distinguish signer from non-signers
   - **Sender anonymity is broken**

3. **Verification Issues**:
   - How are signatures verified?
   - What prevents forging signatures?
   - No clear verification algorithm

4. **XOR-based Response**:
   - Using XOR for cryptographic operations is weak
   - `response = nonce XOR challenge XOR private_key`
   - This is not a standard cryptographic construction

**Attack Vector**: 🔴 **CRITICAL**
- Attacker can identify actual signer
- Attacker can forge signatures
- Sender anonymity completely broken

**Risk Level**: 🔴 **CRITICAL**

---

### 1.4 Hash Functions (SHA256)

**Status**: ✅ **GOOD**

**Implementation**:
```python
import hashlib
hashlib.sha256(data).digest()
```

**Strengths**:
- ✅ SHA256 is cryptographically secure
- ✅ Collision-resistant
- ✅ Standard library implementation

**Weaknesses**:
- ⚠️ Used for multiple purposes without domain separation
- ⚠️ No HMAC for authenticated hashing
- ⚠️ No KDF (key derivation function)

**Risk Level**: 🟡 **MEDIUM**

---

### 1.5 Random Number Generation

**Status**: 🟠 **HIGH RISK** - May not be secure on ESP32

**Current Implementation**:
```python
from nacl.utils import random
nonce = random(32)
```

**Issues**:

1. **ESP32 RNG Quality**:
   - ESP32 has hardware RNG
   - But quality depends on implementation
   - May not be cryptographically secure
   - Entropy source may be predictable

2. **No Entropy Verification**:
   - No check that RNG is working
   - No entropy pool
   - No seed management

3. **Timing Attacks**:
   - RNG may be timing-dependent
   - Predictable under certain conditions

**Attack Vector**: 🟠 **HIGH**
- Attacker predicts random nonces
- Signatures become forgeable
- Ring signatures become linkable

**Risk Level**: 🟠 **HIGH**

---

## PART 2: HARDWARE-LEVEL ATTACKS

### 2.1 Side-Channel Attacks

#### Timing Attacks

**Vulnerability**: Ed25519 operations may leak timing information

**Attack Scenario**:
```
1. Attacker measures time to verify signature
2. Different private keys take different times
3. Attacker derives private key from timing
```

**Current Protection**: ✅ Libsodium uses constant-time operations

**ESP32 Specific Risks**: 🟠 **HIGH**
- Cache timing attacks possible
- Branch prediction attacks possible
- Memory access timing attacks possible
- No cache isolation on ESP32

**Mitigation**:
- ✅ Use libsodium (constant-time)
- ❌ No additional protection on ESP32
- ❌ No cache isolation available

**Risk Level**: 🟠 **HIGH**

---

#### Power Analysis Attacks

**Vulnerability**: Power consumption during cryptographic operations leaks key information

**Attack Scenario**:
```
1. Attacker measures power consumption
2. Different key bits consume different power
3. Attacker derives private key from power trace
```

**Current Protection**: ❌ **NONE**

**ESP32 Specific Risks**: 🔴 **CRITICAL**
- No power isolation
- Power supply directly accessible
- Attacker can measure power draw
- Possible to extract keys via DPA (Differential Power Analysis)

**Mitigation**:
- ❌ No protection possible without hardware changes
- ❌ Can't add masking without significant overhead
- ❌ ESP32 not designed for high-security applications

**Risk Level**: 🔴 **CRITICAL** (if attacker has physical access)

---

#### Electromagnetic Attacks

**Vulnerability**: EM radiation during cryptographic operations leaks information

**Attack Scenario**:
```
1. Attacker measures EM radiation
2. Different operations produce different EM signatures
3. Attacker derives private key from EM trace
```

**Current Protection**: ❌ **NONE**

**ESP32 Specific Risks**: 🔴 **CRITICAL**
- No EM shielding
- No EM hardening
- Possible to measure EM from distance
- Possible to extract keys via EMPA (Electromagnetic Power Analysis)

**Mitigation**:
- ❌ No protection possible without hardware changes
- ❌ Would require Faraday cage
- ❌ Not practical for field deployment

**Risk Level**: 🔴 **CRITICAL** (if attacker has physical proximity)

---

### 2.2 Fault Injection Attacks

**Vulnerability**: Inducing faults during cryptographic operations

**Attack Scenario**:
```
1. Attacker induces fault (voltage glitch, EM pulse)
2. Cryptographic operation fails partially
3. Attacker uses faulty output to derive key
```

**Current Protection**: ❌ **NONE**

**ESP32 Specific Risks**: 🔴 **CRITICAL**
- No fault detection
- No redundancy
- Voltage glitches possible
- EM pulses possible

**Mitigation**:
- ❌ No protection possible without hardware changes
- ❌ Would require voltage regulation and monitoring
- ❌ Would require redundant computation

**Risk Level**: 🔴 **CRITICAL** (if attacker has physical access)

---

### 2.3 Rowhammer Attacks

**Vulnerability**: Bit flips in DRAM via repeated memory access

**Attack Scenario**:
```
1. Attacker accesses memory rows repeatedly
2. Causes bit flips in adjacent rows
3. Flips bits in cryptographic key
4. Derives modified key
```

**Current Protection**: ❌ **NONE**

**ESP32 Specific Risks**: 🟠 **MEDIUM**
- ESP32 has limited DRAM (520 KB)
- Rowhammer less effective on small DRAM
- But still possible with careful targeting

**Mitigation**:
- ❌ No protection possible without hardware changes
- ❌ Would require DRAM ECC
- ❌ Not practical for embedded device

**Risk Level**: 🟠 **MEDIUM** (difficult but possible)

---

## PART 3: KEY MANAGEMENT SECURITY

### 3.1 Key Generation

**Current Implementation**:
```python
signing_key = SigningKey.generate()  # Uses libsodium RNG
```

**Issues**:

1. **RNG Quality on ESP32**:
   - Depends on ESP32 hardware RNG
   - May not have sufficient entropy
   - No entropy verification

2. **No Key Derivation from Seed**:
   - Keys generated directly
   - No BIP32 hierarchical derivation
   - No key recovery from seed phrase

3. **No Key Rotation**:
   - Keys never rotated
   - Compromise = permanent loss

**Risk Level**: 🟠 **HIGH**

---

### 3.2 Key Storage

**Current Implementation**:
```python
self.private_key = bytes(self.signing_key)  # Stored in plaintext RAM
```

**Critical Issues**:

1. **Plaintext in RAM**:
   - Private keys stored unencrypted in RAM
   - Accessible to any process with memory access
   - Accessible to debugger
   - Accessible to memory dump

2. **No Key Zeroization**:
   - Keys not overwritten after use
   - Keys remain in memory
   - Can be recovered from memory dumps

3. **No Secure Enclave**:
   - ESP32 has no secure enclave
   - No hardware-protected key storage
   - No trusted execution environment

4. **No Key Encryption**:
   - Keys not encrypted in memory
   - No key wrapping
   - No key derivation from password

**Attack Vector**: 🔴 **CRITICAL**
- Attacker with memory access gets all keys
- Memory dump reveals all private keys
- Debugger access reveals all keys
- Malware can read all keys

**Risk Level**: 🔴 **CRITICAL**

---

### 3.3 Key Usage

**Current Implementation**:
```python
signature = self.signing_key.sign(message).signature
```

**Issues**:

1. **No Key Isolation**:
   - Key used directly without isolation
   - No key separation between operations
   - No key scheduling

2. **No Audit Trail**:
   - No logging of key usage
   - No detection of unauthorized use
   - No key access control

3. **No Rate Limiting**:
   - Keys can be used unlimited times
   - No rate limiting on signatures
   - No detection of key abuse

**Risk Level**: 🟠 **HIGH**

---

### 3.4 Key Deletion

**Current Implementation**:
```python
# No explicit key deletion
# Keys deleted when object is garbage collected
```

**Issues**:

1. **No Secure Deletion**:
   - Keys not overwritten before deletion
   - Keys may remain in memory
   - Keys may be recovered from swap

2. **No Zeroization**:
   - No explicit memory clearing
   - No use of secure_del or similar
   - Keys persist in memory

3. **No Verification**:
   - No verification that keys are deleted
   - No audit trail of deletion

**Risk Level**: 🔴 **CRITICAL**

---

## PART 4: CONSENSUS SECURITY

### 4.1 DPoP (Delegated Proof-of-Participation) Attacks

**Current Implementation**:
```python
# Validators selected based on stake
# Ring signatures hide sender identity
# Consensus requires 2/3 validator approval
```

**Attack Vectors**:

1. **Validator Collusion**:
   - 2/3 of validators collude
   - Can approve invalid blocks
   - Can fork chain
   - **Mitigation**: Requires honest 1/3

2. **Sybil Attack**:
   - Attacker creates many validators
   - Dilutes voting power
   - Requires stake per validator
   - **Mitigation**: Stake requirement

3. **Long-Range Attack**:
   - Attacker creates alternate chain from genesis
   - Uses old validators that are no longer active
   - Can rewrite entire history
   - **Mitigation**: Checkpoint system needed

4. **Nothing-at-Stake Attack**:
   - Validator votes on multiple forks
   - No penalty for voting on both
   - Can cause consensus failure
   - **Mitigation**: Slashing mechanism needed

**Risk Level**: 🟠 **HIGH** (depends on implementation)

---

### 4.2 Ring Signature Attacks on Consensus

**Current Implementation**:
```python
# Ring signatures hide validator identity
# But ring signature is broken (see 1.3)
```

**Attack Vectors**:

1. **Signer Identification**:
   - Ring signature is broken
   - Attacker can identify actual signer
   - Validator identity revealed
   - **Impact**: Breaks anonymity

2. **Signature Forgery**:
   - Ring signature is broken
   - Attacker can forge signatures
   - Can impersonate validators
   - **Impact**: Consensus broken

3. **Replay Attacks**:
   - No nonce in consensus messages
   - Same signature can be replayed
   - Can cause double-voting
   - **Mitigation**: Add nonce/timestamp

**Risk Level**: 🔴 **CRITICAL**

---

## PART 5: TRANSACTION SECURITY

### 5.1 Double-Spending Attacks

**Current Implementation**:
```python
# UTXO model prevents double-spending
# But no replay protection
```

**Attack Vectors**:

1. **Replay Attack**:
   - Same transaction replayed multiple times
   - UTXO consumed multiple times
   - **Mitigation**: Add nonce/timestamp

2. **Transaction Malleability**:
   - Attacker modifies transaction
   - Changes transaction ID
   - Original sender doesn't recognize it
   - **Mitigation**: Use signature hash

3. **Orphaned Transaction**:
   - Transaction references non-existent UTXO
   - Accepted by some nodes, rejected by others
   - Chain fork
   - **Mitigation**: Validate UTXO existence

**Risk Level**: 🟠 **HIGH**

---

### 5.2 Privacy Attacks

**Current Implementation**:
```python
# Ring signatures hide sender (but broken)
# Stealth addresses hide receiver (but broken)
# Amount encrypted (but key derivation broken)
```

**Attack Vectors**:

1. **Sender Identification**:
   - Ring signature broken
   - Attacker identifies sender
   - **Impact**: Privacy broken

2. **Receiver Identification**:
   - Stealth address broken
   - Attacker identifies receiver
   - **Impact**: Privacy broken

3. **Amount Leakage**:
   - Amount encryption key derivation broken
   - Attacker derives amount
   - **Impact**: Privacy broken

4. **Transaction Linking**:
   - Same sender uses same ring members
   - Transactions linkable
   - **Impact**: Privacy broken

**Risk Level**: 🔴 **CRITICAL**

---

## PART 6: MESHTASTIC LORA SECURITY

### 6.1 LoRa Radio Attacks

**Vulnerability**: LoRa is unencrypted by default

**Attack Scenario**:
```
1. Attacker listens to LoRa traffic
2. Reads all blockchain messages
3. Reads all transaction data
4. Reads all wallet information
```

**Current Protection**: ❌ **NONE**

**Issues**:
- LoRa messages broadcast in plaintext
- No encryption at radio layer
- All data visible to anyone with LoRa receiver
- No authentication of sender

**Mitigation**:
- ✅ Encrypt all messages at application layer
- ✅ Authenticate all messages
- ✅ Add message timestamps
- ✅ Implement message replay protection

**Risk Level**: 🔴 **CRITICAL**

---

### 6.2 LoRa Jamming Attacks

**Vulnerability**: LoRa can be jammed

**Attack Scenario**:
```
1. Attacker transmits on LoRa frequency
2. Blocks all legitimate messages
3. Network becomes unavailable
```

**Current Protection**: ❌ **NONE**

**Mitigation**:
- ✅ Frequency hopping
- ✅ Spread spectrum (already in LoRa)
- ✅ Message redundancy
- ✅ Mesh routing (already in Meshtastic)

**Risk Level**: 🟠 **MEDIUM** (mitigated by LoRa itself)

---

### 6.3 LoRa Spoofing Attacks

**Vulnerability**: LoRa messages can be forged

**Attack Scenario**:
```
1. Attacker sends forged LoRa message
2. Impersonates legitimate node
3. Sends invalid blocks/transactions
```

**Current Protection**: ❌ **NONE** (depends on application)

**Mitigation**:
- ✅ Cryptographic signatures on all messages
- ✅ Message authentication codes
- ✅ Timestamp validation
- ✅ Nonce validation

**Risk Level**: 🔴 **CRITICAL**

---

## PART 7: WALLET SECURITY (PIN-BASED)

### 7.1 PIN Entropy

**Vulnerability**: PIN has low entropy

**Current Implementation** (planned):
```python
# PIN: 4-6 digits
# Entropy: 4 digits = 10^4 = 13 bits
# Entropy: 6 digits = 10^6 = 20 bits
```

**Issues**:
- 4-digit PIN: 10,000 possibilities (brute-forceable)
- 6-digit PIN: 1,000,000 possibilities (brute-forceable)
- No key stretching
- No rate limiting

**Attack Vector**: 🔴 **CRITICAL**
- Attacker tries all 10,000 PINs
- Takes seconds to brute force
- Wallet completely compromised

**Mitigation**:
- ✅ Use Argon2 for key derivation
- ✅ High cost parameters (memory + time)
- ✅ Rate limiting on PIN attempts
- ✅ Lockout after N failed attempts

**Risk Level**: 🔴 **CRITICAL**

---

### 7.2 Key Derivation from PIN

**Vulnerability**: Weak key derivation

**Current Implementation** (planned):
```python
# Likely: key = SHA256(PIN)
# Should be: key = Argon2(PIN, salt, cost=high)
```

**Issues**:
- No salt
- No cost parameter
- No memory hardness
- No time hardness

**Attack Vector**: 🔴 **CRITICAL**
- Attacker precomputes all PIN hashes
- Rainbow table attack
- Instant wallet compromise

**Mitigation**:
- ✅ Use Argon2 with high cost
- ✅ Use random salt per wallet
- ✅ Memory: 64 MB, Time: 3 iterations
- ✅ Verify: 1 second to derive key

**Risk Level**: 🔴 **CRITICAL**

---

### 7.3 Key Storage in SPIFFS

**Vulnerability**: Keys stored in SPIFFS (encrypted)

**Current Implementation** (planned):
```python
# Encrypted with PIN-derived key
# Stored in SPIFFS
```

**Issues**:
- SPIFFS not wear-leveled
- SPIFFS not encrypted at filesystem level
- Encrypted key still vulnerable to side-channel attacks
- No secure deletion

**Attack Vector**: 🟠 **HIGH**
- Attacker extracts SPIFFS
- Brute forces PIN
- Derives key
- Decrypts wallet

**Mitigation**:
- ✅ Use Argon2 for PIN→key derivation
- ✅ Use AES-256-GCM for encryption
- ✅ Use random IV per encryption
- ✅ Implement secure deletion

**Risk Level**: 🟠 **HIGH**

---

## PART 8: SUMMARY OF CRITICAL VULNERABILITIES

### 🔴 CRITICAL ISSUES (Must Fix Immediately)

1. **Ring Signature Broken**
   - Signer can be identified
   - Signatures can be forged
   - Sender anonymity broken
   - **Fix**: Implement standard Schnorr ring signature

2. **Stealth Address ECDH Broken**
   - Not actual ECDH
   - Receiver privacy broken
   - Transactions linkable
   - **Fix**: Implement standard ECDH or use Monero protocol

3. **No Replay Protection**
   - Transactions can be replayed
   - Blocks can be replayed
   - Double-spending possible
   - **Fix**: Add nonce/timestamp to all messages

4. **Keys in Plaintext RAM**
   - Accessible to memory dump
   - Accessible to debugger
   - Accessible to malware
   - **Fix**: Implement key zeroization, consider secure enclave

5. **No PIN Key Derivation**
   - PIN brute-forceable
   - No Argon2 or similar
   - Wallet compromised in seconds
   - **Fix**: Implement Argon2 with high cost

6. **Power Analysis Attacks**
   - Private keys extractable via power measurement
   - No protection on ESP32
   - **Fix**: Use hardware with power isolation (not possible on ESP32)

### 🟠 HIGH PRIORITY ISSUES

1. **Ring Signature Verification**
   - How are signatures verified?
   - What prevents forgery?
   - **Fix**: Implement proper verification algorithm

2. **Hash Function Domain Separation**
   - Multiple uses of SHA256 without domain separation
   - **Fix**: Use HKDF or add domain separation

3. **Random Number Generation**
   - ESP32 RNG quality uncertain
   - **Fix**: Verify RNG quality, use entropy pool

4. **Key Rotation**
   - No key rotation mechanism
   - Compromise = permanent loss
   - **Fix**: Implement key rotation

5. **Timing Attacks on ESP32**
   - Cache timing attacks possible
   - Branch prediction attacks possible
   - **Fix**: Use constant-time operations (libsodium does this)

---

## PART 9: RECOMMENDATIONS

### Immediate Actions (Week 1)

1. **Fix Ring Signature**
   - Replace with standard Schnorr ring signature
   - Implement proper verification
   - Add test vectors

2. **Fix Stealth Address**
   - Implement proper ECDH
   - Use HKDF for key derivation
   - Use standard domain separation

3. **Add Replay Protection**
   - Add nonce to all messages
   - Add timestamp validation
   - Implement nonce cache

4. **Add PIN Key Derivation**
   - Implement Argon2
   - Use high cost parameters
   - Add rate limiting

### Short-term Actions (Week 2-3)

1. **Key Management**
   - Implement key zeroization
   - Add key rotation
   - Add key derivation from seed

2. **Testing**
   - Add cryptographic test vectors
   - Add side-channel tests
   - Add attack scenario tests

3. **Documentation**
   - Document all cryptographic assumptions
   - Document all attack mitigations
   - Document all limitations

### Medium-term Actions (Month 1-2)

1. **Hardware Security**
   - Consider using secure enclave (if available)
   - Implement power analysis mitigation
   - Implement fault injection detection

2. **LoRa Security**
   - Implement message encryption
   - Implement message authentication
   - Implement replay protection

3. **Consensus Security**
   - Implement checkpoint system
   - Implement slashing mechanism
   - Add long-range attack protection

---

## CONCLUSION

The current cryptographic implementation has **critical vulnerabilities** that must be fixed before production deployment:

1. ✅ Ring signature is broken - must be replaced
2. ✅ Stealth address ECDH is broken - must be fixed
3. ✅ No replay protection - must be added
4. ✅ Keys in plaintext RAM - must be mitigated
5. ✅ No PIN key derivation - must be implemented

**Estimated effort to fix all critical issues**: 2-3 weeks

**Recommendation**: Do not proceed to Phase 6 (Wallet) until cryptographic issues are fixed.

