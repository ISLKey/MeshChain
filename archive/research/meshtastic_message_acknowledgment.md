# Meshtastic Message Acknowledgment and Delivery Confirmation Protocols

## Executive Summary

**Yes, Meshtastic contains comprehensive protocols to relay whether messages have been received.** The system implements a multi-layered acknowledgment mechanism that operates at both the zero-hop (direct neighbor) and multi-hop (mesh-wide) levels. Messages display delivery status to users through visual indicators, and the underlying protocol uses **ACK (Acknowledgment)** and **NAK (Negative Acknowledgment)** packets to confirm message delivery.

---

## Part 1: Overview of Acknowledgment Mechanisms

### Core Protocol Components

Meshtastic's acknowledgment system consists of three primary mechanisms:

1. **WantAck Flag**: A protocol-level flag indicating a message requires acknowledgment
2. **ACK Packets**: Explicit acknowledgment messages sent by receiving nodes
3. **Implicit ACKs**: Acknowledgments inferred by observing message rebroadcasting
4. **NAK Packets**: Negative acknowledgments indicating delivery failure
5. **Message Status Indicators**: Visual feedback in client applications

### Protocol Layers

Meshtastic implements acknowledgment at multiple layers:

| Layer | Name | Scope | Mechanism |
|-------|------|-------|-----------|
| **Layer 1** | Unreliable Zero-Hop Messaging | Direct radio transmission | Basic LoRa packet transmission without acknowledgment |
| **Layer 2** | Reliable Zero-Hop Messaging | Direct neighbors only | ACK/NAK for immediate neighbors |
| **Layer 3** | Multi-Hop Messaging | Mesh-wide | Implicit ACKs via rebroadcasting |

---

## Part 2: Layer 2 - Reliable Zero-Hop Messaging (Direct Neighbors)

### The WantAck Flag

The **WantAck flag** is the fundamental mechanism for requesting acknowledgment. When set in a MeshPacket protobuf, it signals:

> "This packet is being sent as a reliable message, we would prefer it to arrive at the destination. We would like to receive an ACK packet in response."

### How Direct Message ACKs Work

When sending a **direct message** (point-to-point) with WantAck enabled:

1. **Sender transmits**: Node A sends a message to Node B with WantAck flag set
2. **Receiver processes**: Node B receives the message and processes it
3. **ACK sent**: Node B sends an explicit ACK packet back to Node A
4. **Confirmation**: Node A receives the ACK and marks the message as delivered
5. **User feedback**: The app displays a checkmark or "Delivered" status

### Retransmission Logic

If the sender does not receive an ACK within a timeout period:

1. **Timeout triggered**: Expiration time based on packet airtime + processing delay
2. **Retransmission**: Message is resent (up to 3 total attempts)
3. **Maximum retries**: After 3 failed attempts, a NAK is generated
4. **User notification**: App displays "Max Retransmissions Reached" error

**Retransmission Parameters:**
- Maximum attempts: 3
- Timeout calculation: Based on airtime of sent packet + processing delay
- Backoff strategy: Exponential (timing increases with each retry)

### Direct Message ACK Example

```
Timeline:
T=0ms:    Node A sends message to Node B (WantAck=true)
T=100ms:  Node B receives message
T=150ms:  Node B sends ACK back to Node A
T=250ms:  Node A receives ACK
Result:   Message marked as "DELIVERED"
```

---

## Part 3: Layer 3 - Multi-Hop Messaging (Broadcasts)

### Implicit ACKs for Broadcast Messages

Broadcast messages (sent to multiple nodes) use a different acknowledgment strategy because **explicit ACKs from all recipients would flood the channel** with traffic.

Instead, Meshtastic uses **implicit ACKs**:

1. **Sender broadcasts**: Node A sends a broadcast message with WantAck flag
2. **Nodes rebroadcast**: Intermediate nodes rebroadcast the message
3. **Implicit ACK**: Sender detects rebroadcasting and infers successful delivery
4. **Confirmation**: If sender hears ANY node rebroadcasting, odds are very high that all nodes will eventually receive it
5. **Timeout**: If no rebroadcast is heard after timeout, message is retransmitted

### Why Implicit ACKs?

**Problem with explicit ACKs:**
- If 100 nodes receive a broadcast, 100 ACKs would be sent back
- This creates a "thundering herd" problem on the channel
- Massive traffic overhead and collisions

**Solution - Implicit ACKs:**
- Only listen for rebroadcasting activity
- Single rebroadcast from any node indicates success
- Minimal overhead while confirming delivery
- Statistically reliable (typical LoRa topology ensures full propagation)

### Broadcast Message Flow

```
Timeline (Broadcast Example):
T=0ms:      Node A broadcasts message (WantAck=true)
T=50-100ms: Nodes B, C, D receive message
T=100-200ms: Nodes B, C, D rebroadcast message
T=150ms:    Node A hears rebroadcast from Node B
T=200ms:    Node A generates implicit ACK
Result:     Message marked as "DELIVERED"
```

### Managed Flooding Algorithm

The rebroadcasting process uses **Managed Flooding** with SNR-based contention:

1. **SNR-based priority**: Nodes with lower SNR (farther away) rebroadcast first
2. **Contention window**: Nodes wait a random time before rebroadcasting
3. **Deduplication**: If a node hears another node rebroadcast, it skips its own
4. **Hop limit**: Message propagates based on HopLimit field (default varies by message type)

---

## Part 4: Message Delivery Status Indicators

### Android App Message States

The Meshtastic Android app displays six distinct message states:

| Status | Icon | Meaning | Details |
|--------|------|---------|---------|
| **UNKNOWN** | ? | Unknown status | Initial state before any feedback |
| **QUEUED** | ⏱️ | Waiting to send | Message queued, device not yet connected |
| **ENROUTE** | ➡️ | In transit | Sent to radio, awaiting ACK/NAK |
| **DELIVERED** | ✓ | Successfully delivered | ACK received from destination |
| **RECEIVED** | ✓✓ | Received and acknowledged | Intended recipient confirmed receipt |
| **ERROR** | ✗ | Delivery failed | NAK received or max retries exceeded |

### iOS/macOS App Indicators

Apple applications provide similar indicators:

- **Acknowledged**: Message received by intended node (orange checkmark, turns grey for direct messages)
- **Unacknowledged**: Message not yet confirmed
- **Failed**: Message delivery failed after retries

### Web Client Status

The Meshtastic Web client displays:
- Message delivery progress
- Acknowledgment status
- Retry attempts
- Error messages

---

## Part 5: Technical Protocol Details

### Packet Header Structure

Every Meshtastic packet includes a header with acknowledgment-related fields:

```
Offset  Length  Field           Purpose
0x00    4 bytes Destination     Target node ID (0xFFFFFFFF for broadcast)
0x04    4 bytes Sender          Source node ID
0x08    4 bytes Packet ID       Unique identifier for this packet
0x0C    1 byte  Flags           Includes WantAck flag (bit 3)
0x0D    1 byte  Channel Hash    For decryption hint
0x0E    1 byte  Next-Hop        For relay routing
0x0F    1 byte  Relay Node      Current relay node
0x10    237B    Payload         Actual message data
```

### WantAck Flag Details

**Bit Position:** Bit 3 of the Flags byte (0x0C)

**Values:**
- `0`: No acknowledgment requested
- `1`: Acknowledgment requested (WantAck enabled)

**Behavior:**
- For direct messages: Explicit ACK sent by recipient
- For broadcasts: Implicit ACK via rebroadcasting
- Automatic retransmission if ACK not received

### ACK/NAK Packet Structure

ACK and NAK packets are special control messages:

**ACK Packet:**
- Sent by recipient to confirm message receipt
- Contains reference to original packet ID
- Routed back to original sender
- Minimal payload (just confirmation)

**NAK Packet:**
- Sent when delivery fails
- Contains error code indicating failure reason
- Examples: "Max Retransmissions Reached", "Delivery Failed"
- Triggers user notification

---

## Part 6: Acknowledgment Behavior by Message Type

### Direct Messages (Point-to-Point)

**Default behavior:**
- WantAck enabled by default
- Explicit ACK sent by recipient
- Retransmitted up to 3 times if no ACK
- User sees checkmark when delivered

**Example:**
```
User A → User B (direct message)
- Message sent with WantAck=true
- User B receives and app confirms
- User B's device sends ACK
- User A sees "DELIVERED" status
```

### Broadcast Messages

**Default behavior:**
- WantAck enabled by default
- Implicit ACK via rebroadcasting
- No explicit ACKs from recipients
- User sees checkmark when rebroadcast detected

**Example:**
```
User A → All nodes (broadcast)
- Message sent with WantAck=true
- Nodes B, C, D receive and rebroadcast
- User A detects rebroadcast from any node
- User A sees "DELIVERED" status
- No ACKs sent back (prevents flooding)
```

### Channel Messages

**Behavior:**
- Can be sent with or without WantAck
- Treated as broadcasts
- Implicit ACK via rebroadcasting
- Limited ACK information (can't see who specifically received)

---

## Part 7: Advanced Features

### Next-Hop Routing (Firmware 2.6+)

Modern Meshtastic firmware uses **Next-Hop Routing** for improved efficiency:

1. **Initial delivery**: Uses managed flooding to reach destination
2. **Response tracking**: Monitors which node relayed the response
3. **Next-hop designation**: Marks that node as preferred relay
4. **Optimized retries**: Uses next-hop for subsequent messages
5. **Fallback**: Returns to managed flooding if next-hop fails

**Benefits:**
- Reduced retransmissions
- Lower latency
- Better mesh efficiency
- Automatic adaptation to network changes

### Traceroute Feature

Users can perform **traceroute** to see the actual path a message takes:

```
Command: meshtastic --traceroute <node_id>

Response shows:
- Each hop in the path
- SNR at each hop
- Hop timing
- Confirmation of delivery
```

### Store and Forward Module

For offline nodes, Meshtastic includes a **Store and Forward module**:

1. **Message storage**: Gateway nodes store messages for offline recipients
2. **Delayed delivery**: Messages delivered when recipient comes online
3. **Acknowledgment**: ACK sent when message is finally delivered
4. **Timeout**: Messages expire after configurable period

---

## Part 8: Reliability Characteristics

### Delivery Guarantees

Meshtastic provides **best-effort delivery** with the following characteristics:

| Aspect | Guarantee | Details |
|--------|-----------|---------|
| **Direct Messages** | High reliability | ACK/NAK confirmation, up to 3 retries |
| **Broadcasts** | Best effort | Implicit ACK via rebroadcasting |
| **Multi-hop** | Probabilistic | Depends on network topology and hop count |
| **Offline nodes** | No guarantee | Message lost if recipient offline (unless Store & Forward enabled) |
| **Encryption** | Transparent | ACKs work with encrypted messages |

### Factors Affecting Delivery

| Factor | Impact | Mitigation |
|--------|--------|-----------|
| **Distance** | Increased failure rate | Mesh relays message through intermediate nodes |
| **Interference** | Packet loss | Retransmission mechanism handles this |
| **Hop count** | Exponential failure increase | Managed flooding reduces impact |
| **Network congestion** | Collision and delays | CSMA/CA mechanism reduces collisions |
| **Node offline** | Permanent failure | Store and Forward module can help |

---

## Part 9: Practical Examples

### Example 1: Direct Message Delivery

```
Scenario: Alice sends message to Bob (direct neighbors)

Step 1: Alice composes message
- App creates MeshPacket with WantAck=true
- Destination = Bob's Node ID
- Payload = "Hello Bob"

Step 2: Message transmission
- Alice's device sends packet via LoRa
- Airtime: ~200ms (depends on packet size)

Step 3: Bob receives
- Bob's device receives packet
- Decrypts and displays message
- Generates ACK packet

Step 4: ACK transmission
- Bob's device sends ACK back to Alice
- Airtime: ~50ms (small ACK packet)

Step 5: Alice receives ACK
- Alice's device receives ACK
- Matches ACK to original message ID
- Updates message status to "DELIVERED"
- App shows checkmark

Total time: ~300-400ms
User feedback: Immediate checkmark
```

### Example 2: Broadcast to Mesh

```
Scenario: Alice broadcasts message to all nodes

Step 1: Alice composes broadcast
- App creates MeshPacket with WantAck=true
- Destination = 0xFFFFFFFF (broadcast)
- Payload = "Attention everyone!"

Step 2: Message transmission
- Alice's device sends broadcast packet
- Airtime: ~200ms

Step 3: Nodes receive and rebroadcast
- Nodes B, C, D receive packet
- Each waits random time (SNR-based)
- Node D (farthest) rebroadcasts first
- Nodes B, C hear rebroadcast, skip their own

Step 4: Alice detects rebroadcast
- Alice's device hears Node D rebroadcasting
- Generates implicit ACK
- Updates message status to "DELIVERED"

Step 5: Further propagation
- Node D's rebroadcast reaches Nodes E, F
- They rebroadcast to Nodes G, H
- Message propagates through mesh

Total time: ~500-1000ms (depends on mesh size)
User feedback: Checkmark when first rebroadcast heard
Reliability: Very high (statistically proven)
```

### Example 3: Failed Delivery with Retry

```
Scenario: Alice sends to Bob, but message lost initially

Step 1: First transmission
- Alice sends message to Bob
- Bob's device is temporarily off-channel
- No ACK received

Step 2: Timeout (T+500ms)
- Alice's device detects no ACK
- Retransmits message (attempt 2 of 3)

Step 3: Second transmission
- Message sent again
- Bob's device still not receiving
- No ACK received

Step 4: Timeout (T+1000ms)
- Alice's device retransmits (attempt 3 of 3)

Step 5: Third transmission
- Message finally reaches Bob
- Bob sends ACK

Step 6: Success or failure
- If ACK received: Status = "DELIVERED"
- If no ACK after 3 attempts: Status = "ERROR"

Total time: ~1500ms
User feedback: Delayed checkmark or error message
```

---

## Part 10: Configuration and Customization

### Enabling/Disabling ACKs

Users can control acknowledgment behavior:

```bash
# Enable ACK for a channel (default)
meshtastic --ch-index 0 --ch-set want_ack true

# Disable ACK (for broadcast-only channels)
meshtastic --ch-index 0 --ch-set want_ack false
```

### Timeout Configuration

Advanced users can adjust timeout values (requires firmware modification):

- Default timeout: Based on packet airtime + 500ms
- Minimum timeout: ~200ms
- Maximum timeout: ~5000ms
- Adjustable per device in firmware

### Retry Behavior

Current implementation:
- Maximum retries: 3 (hardcoded)
- Retry timing: Exponential backoff
- No user-configurable retry count (by design)

---

## Part 11: Limitations and Considerations

### Broadcast Acknowledgment Limitations

1. **No per-recipient confirmation**: You don't know which specific nodes received the message
2. **Implicit only**: Can't distinguish between "received" and "rebroadcasted"
3. **Flooding dependency**: Relies on network topology for rebroadcasting
4. **No delivery guarantee**: Doesn't guarantee all nodes received the message

### Direct Message Limitations

1. **Neighbor-only ACK**: Only immediate neighbors can send ACK
2. **Hop-limited**: Multi-hop messages may not get ACKs
3. **Offline nodes**: No ACK if recipient is offline
4. **Encryption overhead**: ACKs still subject to encryption delays

### Network Limitations

1. **Congestion**: High traffic reduces ACK reliability
2. **Interference**: RF interference can corrupt ACKs
3. **Asymmetric links**: Forward path may work but return path may fail
4. **Timing**: ACKs may be delayed in congested networks

---

## Part 12: Comparison with Other Systems

### vs. SMS/Cellular

| Feature | Meshtastic | SMS |
|---------|-----------|-----|
| **ACK mechanism** | Protocol-level | Server-based |
| **Delivery confirmation** | Mesh-aware | Network-based |
| **Offline handling** | Mesh relay | Server storage |
| **Reliability** | Best-effort | High (infrastructure) |

### vs. LoRaWAN

| Feature | Meshtastic | LoRaWAN |
|---------|-----------|---------|
| **ACK type** | Peer-to-peer | Gateway-based |
| **Mesh support** | Native | Not supported |
| **Broadcast ACK** | Implicit | Not supported |
| **Multi-hop** | Managed flooding | Single hop |

### vs. Traditional Mesh Networks

| Feature | Meshtastic | Traditional Mesh |
|---------|-----------|-----------------|
| **ACK protocol** | Simple, efficient | Complex routing |
| **Overhead** | Minimal | Higher |
| **Reliability** | Good for small networks | Better for large networks |
| **Implementation** | Lightweight | Resource-intensive |

---

## Conclusion

Meshtastic implements a **sophisticated and efficient acknowledgment system** that balances reliability with network efficiency. The use of explicit ACKs for direct messages and implicit ACKs for broadcasts represents an elegant solution to the challenges of mesh networking.

Key takeaways:

1. **Comprehensive coverage**: Both direct and broadcast messages have acknowledgment mechanisms
2. **User-visible feedback**: Apps display clear status indicators for each message
3. **Automatic retransmission**: Failed messages are automatically retried up to 3 times
4. **Network-aware**: ACK behavior adapts to message type (direct vs. broadcast)
5. **Efficient**: Implicit ACKs prevent channel flooding while maintaining reliability
6. **Transparent**: Works seamlessly with encryption and multi-hop routing

For users, this means **reliable message delivery confirmation** with minimal overhead, making Meshtastic suitable for both casual communication and critical applications where delivery confirmation is essential.
