# PiRowFlo Installation and Usage Guide

This document preserves a known working PiRowFlo configuration for Raspberry Pi.
It exists so you never have to repeat the BLE troubleshooting process again.

Repository:
https://github.com/pentecosthub/PiRowFlo

Known working tag:
pirowflo-working-ble

--------------------------------------------------
SUPPORTED HARDWARE
--------------------------------------------------

- Raspberry Pi 4 or 5
- WaterRower with S4 monitor
- Built-in Raspberry Pi Bluetooth
- Optional ANT+ USB dongle (receive is limited)

--------------------------------------------------
OPERATING SYSTEM
--------------------------------------------------

- Raspberry Pi OS 64-bit
- Bluetooth enabled
- Internet access during install

--------------------------------------------------
INSTALLATION
--------------------------------------------------

1. Update system

sudo apt update
sudo apt upgrade -y

2. Install required packages

sudo apt install -y git python3 python3-pip python3-dbus python3-gi bluez bluetooth libglib2.0-dev

3. Enable Bluetooth

sudo systemctl enable bluetooth
sudo systemctl start bluetooth

4. Clone repository

git clone https://github.com/pentecosthub/PiRowFlo.git
cd PiRowFlo

5. Checkout known working release

git checkout pirowflo-working-ble

6. Install Python dependencies

pip3 install -r requirements.txt

7. Enable and start PiRowFlo service

sudo systemctl enable pirowflo
sudo systemctl start pirowflo

--------------------------------------------------
CORRECT STARTUP ORDER (IMPORTANT)
--------------------------------------------------

1. Power on WaterRower and S4 monitor
2. Wait until S4 is fully booted
3. Power on Raspberry Pi
4. Wait 30 to 60 seconds
5. Open rowing or fitness app
6. Scan for Bluetooth devices
7. Connect to PiRowFlo

BLE advertising may take up to one minute. This is normal.

--------------------------------------------------
BLUETOOTH NOTES
--------------------------------------------------

- Device name: PiRowFlo
- BLE services:
  - Fitness Machine (0x1826)
  - Heart Rate (0x180D)

bluetoothctl may show:
Discoverable: no

This does NOT mean BLE advertising is broken.

--------------------------------------------------
HEART RATE MONITORS
--------------------------------------------------

Bluetooth heart rate straps should be paired to the PHONE or APP, not PiRowFlo.

Correct workflow:
1. Pair HR strap to phone or app
2. Connect app to PiRowFlo
3. App merges rowing and heart rate data

--------------------------------------------------
VERIFICATION
--------------------------------------------------

Check service status:

sudo systemctl status pirowflo

Monitor BLE advertising:

sudo btmon

You should see:
- Advertising enabled
- PiRowFlo name
- Fitness Machine and Heart Rate UUIDs

--------------------------------------------------
RECOVERY
--------------------------------------------------

If the SD card fails:

1. Reinstall Raspberry Pi OS
2. Repeat install steps
3. Checkout pirowflo-working-ble tag
4. Do NOT modify BLE code

--------------------------------------------------
KNOWN LIMITATIONS
--------------------------------------------------

- ANT+ heart rate receive not fully implemented
- BLE advertising may be delayed
- Bluetooth status output can be misleading

--------------------------------------------------
MAINTENANCE
--------------------------------------------------

No further changes are required.
This repository exists to preserve a working state.
