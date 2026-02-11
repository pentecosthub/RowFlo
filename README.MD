# RowFlo - Device-Neutral WaterRower Broadcaster

> **Note:** RowFlo uses WaterRower's native Bluetooth Low Energy protocol for reliable data transmission. 
> An FTMS implementation was attempted but abandoned due to data flow issues. See `DECISIONS.md` for details.

## What RowFlo Does

RowFlo is a stable, device-neutral Linux application that:
- Reads WaterRower S4 monitor data via USB serial connection
- Broadcasts rowing metrics via Bluetooth Low Energy using WaterRower's native protocol
- Works on any Linux system (Ubuntu, Debian, Raspberry Pi OS)
- Auto-starts on boot and runs headless

## What RowFlo Does NOT Do

- Does not use FTMS (Fitness Machine Service) protocol
- Does not receive Bluetooth or ANT+ heart rate data
- Does not support SmartRow input (removed for stability)
- Does not aggregate multiple input sources

## Project Goal

Create a maintainable fork of PiRowFlo focused on:
- **Device neutrality** - Remove Raspberry Pi-specific dependencies
- **Stability** - Simplified architecture, reliable operation
- **Portability** - Works across Linux distributions and hardware platforms

## Compatibility

### Tested Systems
- ✅ Ubuntu 22.04 LTS (Dell Optiplex 3050, x86_64)
- ✅ Raspberry Pi OS (Raspberry Pi 3B, ARM)
- ✅ Ubuntu 24.04 LTS (expected to work)

### Bluetooth Requirements
- Bluetooth 4.0+ adapter (BLE support required)
- Internal or USB Bluetooth adapter
- Avoid using multiple Bluetooth adapters simultaneously (causes conflicts)

### Compatible Apps
Apps that support WaterRower's native BLE protocol:
- WaterRower Connect app
- Other WaterRower-compatible fitness apps

Apps that require FTMS protocol will NOT work (Peloton, Zwift, etc.)

## Installation

### Prerequisites
```bash
