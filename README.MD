# RowFlo - Device-Neutral WaterRower Broadcaster


## What RowFlo Does

RowFlo is a stable, device-neutral Linux application that:
- Reads WaterRower S4 monitor data via USB serial connection
- Broadcasts rowing metrics via Bluetooth Low Energy using WaterRower's native protocol
- Works on any Linux system (Ubuntu, Debian, Raspberry Pi OS)
- Auto-starts on boot and runs headless

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

## Installation

### Prerequisites

**System Requirements:**
- Linux-based operating system (Ubuntu, Debian, Raspberry Pi OS)
- Bluetooth 4.0+ adapter
- Python 3.10 or newer
- WaterRower S4 monitor with USB cable

**Install required system packages:**
```bash
sudo apt update
sudo apt install git bluez bluetooth python3 python3-pip python3-venv
```

### Quick Install
```bash
# Clone the repository
cd ~
git clone https://github.com/pentecosthub/RowFlo.git
cd RowFlo

# Run the installation script
./install.sh
```

The installation script will:
- Install all required system packages
- Create a Python virtual environment
- Install Python dependencies
- Create logging configuration
- Set up systemd service for auto-start
- Add your user to required groups (bluetooth, dialout)

**Important:** You must log out and log back in for group changes to take effect.

### Post-Installation

After logging back in, RowFlo will start automatically on boot.

**Check service status:**
```bash
sudo systemctl status rowflo
```

**View live logs:**
```bash
sudo journalctl -u rowflo -f
```

**Restart service:**
```bash
sudo systemctl restart rowflo
```

### Usage

1. **Plug in your WaterRower S4 USB cable**
2. **RowFlo auto-starts** and begins broadcasting
3. **Open WaterRower-compatible app** on your phone/tablet
4. **Scan for Bluetooth devices** and connect to "RowFlo"
5. **Start rowing!**

The service runs headless - no monitor or keyboard needed after setup.

### Troubleshooting

See [KNOWN_ISSUES.md](KNOWN_ISSUES.md) for common problems and solutions.

**Bluetooth not working?**
```bash
sudo rfkill unblock bluetooth
sudo systemctl restart bluetooth
sudo systemctl restart rowflo
```

**Service won't start?**
```bash
# Check logs for errors
sudo journalctl -u rowflo -n 50
```

## License and Attribution

RowFlo is licensed under the GNU General Public License v3.0 (GPL-3.0).

This project is a fork of [PiRowFlo](https://github.com/inonoob/pirowflo/) by inonoob and contributors.

### Modifications from Original PiRowFlo

- Removed Raspberry Pi-specific dependencies for device-neutral operation
- Removed supervisord in favor of simple systemd service
- Removed SmartRow input support (focus on WaterRower S4 only)
- Removed ANT+ broadcasting support
- Updated installation process for broader Linux compatibility
- Added comprehensive documentation for device-neutral deployment
- Attempted and abandoned FTMS protocol implementation (see DECISIONS.md)

### Copyright

Original PiRowFlo: Copyright © inonoob and contributors  
RowFlo modifications: Copyright © 2026 pentecosthub

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

See [LICENSE](LICENSE) file for full license text.


```bash
