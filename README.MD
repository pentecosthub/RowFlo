# RowFlo

RowFlo is a device-neutral fork of PiRowFlo.

This fork focuses on maintaining existing functionality while removing hard-coded Raspberry Pi assumptions, improving installation documentation, and increasing portability across Linux-based systems.

## Features

* Read serial WaterRower data via USB (S4 Monitor)
* Broadcast rowing data over Bluetooth Low Energy using FTMS protocol
* Broadcast rowing data over ANT+ using compatible dongles
* Receive heart rate data from ANT+ heart rate straps
* Web-based configuration interface on port 9001
* Command-line interface for manual control

## Compatibility

### Fitness Apps (via FTMS/BLE)

RowFlo broadcasts rowing data using the standard Fitness Machine Service (FTMS) protocol over Bluetooth Low Energy. This means it works with **any app that supports FTMS-compatible rowing machines**.

Confirmed working apps include:
* **Peloton** (requires App+ or All-Access membership)
* **Kinomap**
* **Holofit**
* **Cityrowgo**
* **WaterRower Connect**
* **Coxswain** (version 7.9 or higher)
* **EXR**

Many other fitness apps with FTMS support should also work.

### Fitness Watches & Devices (via ANT+)

* **Garmin watches** with ANT+ and rowing activity profiles
* **ANT+ heart rate monitors** (RowFlo receives HR data from straps)

## Requirements

### Hardware

RowFlo works on any Linux-based system with:
* USB port (for S4 Monitor connection)
* Bluetooth Low Energy adapter (built-in or USB)
* Optional: ANT+ USB dongle (for Garmin watch support and HR strap input)

Compatible systems include:
* Raspberry Pi (all models with Bluetooth)
* Intel NUC and other mini PCs
* Thin clients
* Standard desktop/laptop Linux systems
* Any x86_64 or ARM64 Linux computer

### Software

* Linux OS (tested on Ubuntu 22.04+, Raspberry Pi OS, Debian)
* Python 3.8 or higher
* Bluetooth/BlueZ stack
* systemd (for automatic startup)

## Installation

### Quick Install
```bash
sudo apt-get update
sudo apt-get install git
git clone https://github.com/pentecosthub/RowFlo.git
cd RowFlo
chmod +x install.sh
./install.sh
```

**Important:** After installation, log out and log back in for group permissions to take effect.

### Starting RowFlo

Automatic (via systemd):
```bash
sudo systemctl start supervisord
```

Manual (for testing):
```bash
venv/bin/python3 src/waterrowerthreads.py -i s4 -b -a
```

### Web Interface

Access at: `http://<device-ip>:9001`

Find your IP: `hostname -I`

## Command Line Options
```bash
venv/bin/python3 src/waterrowerthreads.py [OPTIONS]

Options:
  -i, --interface {s4}    Interface type (S4 Monitor)
  -b, --blue             Enable BLE broadcasting (FTMS)
  -a, --antfe            Enable ANT+ broadcasting and HR receiving
  -h, --help             Show help
```

Examples:
```bash
# BLE only (for Peloton, Kinomap, etc.)
venv/bin/python3 src/waterrowerthreads.py -i s4 -b

# ANT+ only (Garmin watches)
venv/bin/python3 src/waterrowerthreads.py -i s4 -a

# Both BLE and ANT+ (maximum compatibility)
venv/bin/python3 src/waterrowerthreads.py -i s4 -b -a
```

## Troubleshooting

### Serial open error
```bash
sudo usermod -a -G dialout $USER
```
Then log out and log back in.

### Bluetooth permission errors
```bash
sudo usermod -a -G bluetooth $USER
```
Then log out and log back in.

### ANT+ dongle not detected
```bash
lsusb | grep -i ant
sudo usermod -a -G plugdev $USER
```

Avoid Cyclone chipset dongles - use Dynastream/Garmin branded dongles.

### Web interface not accessible
```bash
sudo systemctl status supervisord
sudo systemctl restart supervisord
```

## Device Neutrality

RowFlo works across different Linux platforms:

* No Raspberry Pi GPIO dependencies
* No hard-coded Pi-specific paths
* Works with any Bluetooth adapter
* Standard systemd service configuration
* Python virtual environment for dependency isolation

Run RowFlo on: Raspberry Pi, laptops, desktop PCs, mini PCs, thin clients, or any Linux system.

## Code Attribution

Based on code from:

* [waterrower](https://github.com/bfritscher/waterrower) - WaterRower serial communication
* [espresso-ble](https://github.com/PunchThrough/espresso-ble) - BLE GATT server
* [FortiusANT](https://github.com/WouterJD/FortiusANT) - ANT+ Fitness Equipment protocol

## License

GPL-3.0 - See LICENSE file for details.
