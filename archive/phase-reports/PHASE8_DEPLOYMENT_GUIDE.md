# Phase 8: Testnet Deployment Guide

## Overview

This guide provides comprehensive instructions for deploying MeshChain on 5-6 ESP32 devices running Meshtastic firmware.

## Prerequisites

### Hardware Requirements

- **5-6 ESP32 devices** (ESP32, ESP32-S3, or compatible)
- **Meshtastic firmware** pre-installed on each device
- **USB cables** for serial communication
- **microSD cards** (optional, for extended storage)
- **LoRa antennas** for mesh communication

### Software Requirements

- Python 3.8+
- MeshChain repository cloned
- All dependencies installed (`pip install -r requirements.txt`)

### Network Requirements

- All devices should be within LoRa range (typically 1-10 km depending on terrain)
- Devices will communicate via LoRa mesh network (no internet required)

## Deployment Steps

### Step 1: Prepare Genesis Block

```python
from meshchain.genesis import TestnetGenesisBuilder

# Create 5-node testnet
genesis_block = TestnetGenesisBuilder.create_5_node_testnet()

# Or create 6-node testnet
genesis_block = TestnetGenesisBuilder.create_6_node_testnet()

# Save genesis block
with open('genesis.json', 'w') as f:
    json.dump(genesis_block, f, indent=2)
```

### Step 2: Create Device Configurations

```python
from meshchain.device_config import TestnetConfigBuilder

# Create 5-node configuration
config_manager = TestnetConfigBuilder.create_5_node_testnet()

# Or create 6-node configuration
config_manager = TestnetConfigBuilder.create_6_node_testnet()

# Save configurations
config_manager.save_to_file('device_configs.json')
```

### Step 3: Setup Validators

```python
from meshchain.testnet_validators import TestnetValidatorSetup

# Setup 5-node validators
validator_manager = TestnetValidatorSetup.setup_5_node_validators()

# Or setup 6-node validators
validator_manager = TestnetValidatorSetup.setup_6_node_validators()

# Save validator configurations
validator_manager.save_to_file('validators.json')
```

### Step 4: Validate Configuration

```python
from meshchain.testnet_validation import TestnetValidator

validator = TestnetValidator()

# Validate genesis block
is_valid, errors = validator.validate_genesis_block(genesis_block)
if not is_valid:
    print("Genesis block validation failed:")
    for error in errors:
        print(f"  - {error}")

# Validate device configurations
is_valid, errors = validator.validate_device_configs(device_configs)
if not is_valid:
    print("Device configuration validation failed:")
    for error in errors:
        print(f"  - {error}")

# Validate network topology
is_valid, errors = validator.validate_network_topology(device_configs)
if not is_valid:
    print("Network topology validation failed:")
    for error in errors:
        print(f"  - {error}")
```

### Step 5: Bootstrap Devices

```python
from meshchain.bootstrap import TestnetBootstrapper

# Create testnet bootstrapper
bootstrapper = TestnetBootstrapper(testnet_config)

# Bootstrap all devices
success = bootstrapper.bootstrap_all_devices()

# Save bootstrap status
bootstrapper.save_status('bootstrap_status.json')
```

### Step 6: Monitor Health

```python
from meshchain.testnet_validation import TestnetHealthMonitor

monitor = TestnetHealthMonitor()

# Check device connectivity
monitor.check_device_connectivity('device-1', is_connected=True)

# Check network latency
monitor.check_network_latency(latency_ms=150.0)

# Check block production
monitor.check_block_production(blocks_per_minute=6.0)

# Check consensus health
monitor.check_consensus_health(validators_online=5, total_validators=5)

# Get health report
health_report = monitor.get_health_report()
print(f"Overall health: {health_report['overall_status']}")
```

### Step 7: Run Stress Tests (Optional)

```python
from meshchain.testnet_simulator import StressTestRunner

# Run 5-node stress test
results = StressTestRunner.test_5_node_network()
print(f"5-node test: {results['summary']['total_blocks']} blocks produced")

# Run 6-node stress test
results = StressTestRunner.test_6_node_network()
print(f"6-node test: {results['summary']['total_blocks']} blocks produced")
```

## Configuration Files

### genesis.json

Contains the genesis block for the testnet:

```json
{
  "version": 1,
  "height": 0,
  "timestamp": 1234567890,
  "parent_hash": "0000...",
  "testnet_name": "meshchain-5node-testnet",
  "validators": [
    {
      "node_id": 287454545,
      "stake": 10000,
      "public_key": "aaaa...",
      "description": "Validator 1"
    }
  ],
  "utxos": [
    {
      "owner": 287454545,
      "amount": 1000,
      "description": "Initial allocation"
    }
  ]
}
```

### device_configs.json

Contains configuration for each device:

```json
{
  "device-1": {
    "device_id": "device-1",
    "hardware": {
      "device_type": "ESP32",
      "ram_mb": 240,
      "storage_mb": 4096
    },
    "network": {
      "node_id": 287454545,
      "device_name": "Validator-1",
      "serial_port": "/dev/ttyUSB0"
    },
    "blockchain": {
      "role": "validator",
      "is_validator": true,
      "validator_stake": 10000
    }
  }
}
```

### validators.json

Contains validator configurations:

```json
{
  "0x11111111": {
    "node_id": "0x11111111",
    "status": "active",
    "keys": {
      "public_key": "aaaa...",
      "signing_key": "aaaa..."
    },
    "stake": {
      "amount": 10000,
      "withdrawal_address": "0x11111111"
    }
  }
}
```

## Troubleshooting

### Device Not Connecting

1. Check USB cable connection
2. Verify serial port is correct (`/dev/ttyUSB*` on Linux, `COM*` on Windows)
3. Check Meshtastic firmware is installed and running
4. Try different USB port

### Genesis Block Validation Fails

1. Check all validators are configured
2. Verify total stake is > 0
3. Check all UTXOs are valid
4. Ensure genesis block hash is correct

### Bootstrap Fails

1. Check device configurations are valid
2. Verify all required fields are present
3. Check storage path is accessible
4. Ensure wallet creation succeeds

### Network Issues

1. Check all devices are within LoRa range
2. Verify mesh channel is same on all devices
3. Check antenna connections
4. Monitor signal strength (RSSI)

## Performance Tuning

### Block Time

Default: 10 seconds per block

To adjust, modify `TESTNET_BLOCK_TIME` in `genesis.py`:

```python
TESTNET_BLOCK_TIME = 10  # Change to desired value
```

### Maximum Block Size

Default: 1 MB

To adjust, modify `TESTNET_MAX_BLOCK_SIZE` in `genesis.py`:

```python
TESTNET_MAX_BLOCK_SIZE = 1000000  # Change to desired value
```

### Peer Limits

Default: 10 peers per device

To adjust, modify device configuration:

```python
config.blockchain.max_peers = 20  # Change to desired value
```

## Monitoring and Logging

### Enable Debug Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

### Monitor Block Production

```python
# Check block height on each device
for device_id, device in devices.items():
    print(f"{device_id}: height={device.block_height}")
```

### Monitor Network Connectivity

```python
# Check peer count on each device
for device_id, device in devices.items():
    print(f"{device_id}: peers={len(device.peers)}")
```

## Deployment Checklist

- [ ] Hardware prepared (5-6 ESP32 devices with Meshtastic)
- [ ] Genesis block created and validated
- [ ] Device configurations created and validated
- [ ] Validators configured and validated
- [ ] Network topology validated
- [ ] Devices bootstrapped successfully
- [ ] Health checks passing
- [ ] Stress tests completed (optional)
- [ ] Monitoring system running
- [ ] Logging enabled
- [ ] Backup of all configurations created

## Next Steps

After successful deployment:

1. Monitor network health continuously
2. Collect performance metrics
3. Test transaction throughput
4. Test consensus under various conditions
5. Document any issues or improvements
6. Prepare for production deployment

## Support and Issues

For issues or questions:

1. Check the troubleshooting section above
2. Review log files for error messages
3. Verify all configurations are correct
4. Run validation checks again
5. Contact the development team

## Additional Resources

- [MeshChain Documentation](README.md)
- [Meshtastic Documentation](https://meshtastic.org/)
- [ESP32 Documentation](https://docs.espressif.com/projects/esp-idf/)
