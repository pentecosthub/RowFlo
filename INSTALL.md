# PiRowFlo Installation Guide

This document describes how to install and run a known working BLE version of PiRowFlo on a Raspberry Pi.

---

## System Requirements

- Raspberry Pi with built-in Bluetooth (Pi 3, 4, 5)
- Raspberry Pi OS (Bookworm or Bullseye)
- Internet connection
- WaterRower S4 monitor
- BLE-compatible rowing app (WaterRower app, ErgData, etc.)
- https://www.raspberrypi.com/software/ to format an sd card with raspbian

---

## Installation Steps

### 1. Update system

```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Install required packages

```bash
sudo apt install -y git python3 python3-pip python3-dbus python3-gi bluez bluetooth libglib2.0-dev
```

### 3. Enable Bluetooth

```bash
sudo systemctl enable bluetooth
sudo systemctl start bluetooth
```

### 4. Clone the PiRowFlo repository

```bash
git clone https://github.com/pentecosthub/PiRowFlo.git
cd PiRowFlo
```

### 5. Checkout the known working BLE release

```bash
git checkout pirowflo-working-ble
```

### 6. Install Python dependencies

```bash
pip3 install -r requirements.txt
```

### 7. Enable and start the PiRowFlo service

```bash
sudo systemctl enable pirowflo
sudo systemctl start pirowflo
```

---

## Startup Order (Important)

1. Power on the WaterRower and ensure the S4 monitor is connected
2. Power on the Raspberry Pi
3. Wait 30–60 seconds for Bluetooth advertising to stabilize
4. Open the rowing app on your phone
5. Scan for BLE devices and connect to **PiRowFlo**

Do not panic if the device does not appear immediately. BLE advertising can take up to one minute to become visible.

---

## Verifying Operation

To confirm PiRowFlo is running:

```bash
sudo systemctl status pirowflo
```

To monitor Bluetooth activity:

```bash
sudo btmon
```

To view service logs:

```bash
sudo journalctl -u pirowflo -f
```

---

## Known Working State

This repository includes a Git tag representing a verified working BLE configuration:

- Tag: `pirowflo-working-ble`

This tag confirms:
- BLE advertising is functional
- GATT services are registered correctly
- Phone apps can discover and connect
- No ANT+ heart rate dependency is required

---

## Notes

- Heart rate straps should be paired directly to the phone app, not to PiRowFlo
- ANT+ receive is not currently supported and should be considered non-functional
- BLE advertising may take up to 60 seconds after service start

---

## Recovery

If the SD card fails or the system must be rebuilt, repeat the steps in this document and checkout the same tag.

```bash
git checkout pirowflo-working-ble
```

This will restore a known-good configuration.

---
