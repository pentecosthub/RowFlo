# RowFlo v0.1 Known Issues

This file documents limitations inherited from PiRowFlo that prevent full device neutrality.

## Raspberry Pi Only Components

1. OLED Screen System  
The screen adapter depends on SPI, luma.oled, and RPi.GPIO. These libraries only exist on Raspberry Pi.

2. screen.service  
The systemd service at services/screen.service assumes Raspberry Pi hardware and will not work on generic Linux.

3. install.sh modifies Raspberry Pi boot config  
The installer edits /boot/firmware/config.txt which does not exist on standard Linux systems.

## SmartRow

SmartRow support is currently disabled due to broken adapter code that does not run on modern Python.

## What Works

S4 USB rowing, BLE broadcasting, and ANT+ broadcasting run correctly on generic Linux systems such as Ubuntu 24.04.

## Logging system prevents startup

On Ubuntu 24.04 and modern Python, RowFlo fails during startup with:

KeyError: 'formatters'

The file src/logging.conf is not compatible with Python's logging.config.fileConfig
format and causes RowFlo to crash before any services start.
