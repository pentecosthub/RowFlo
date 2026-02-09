# RowFlo Changelog

## [Unreleased] - Device-Neutral Conversion

### Added
- Device-neutral installation script that works on any Linux system
- Peloton app support documentation
- General FTMS compatibility statement for any FTMS-supporting app
- Python virtual environment for dependency isolation
- Clearer documentation about ANT+ heart rate strap receiving

### Changed
- Updated README to focus on FTMS protocol compatibility
- Simplified requirements.txt (removed Pi-specific dependencies)
- Install script now works on Ubuntu, Debian, Raspberry Pi OS, and other Linux distributions
- Bluetooth device name changed from "PiRowFlo" to "RowFlo"

### Removed
- Screen adapter (OLED display support with physical buttons)
- All Raspberry Pi GPIO dependencies
- luma.oled library requirement
- RPI.GPIO library requirement
- Hard-coded Raspberry Pi assumptions
- Specific watch model list (replaced with general Garmin ANT+ support statement)

### Technical Details
- Removed 1,167 lines of Pi-specific code
- Added 305 lines of device-neutral code
- All core functionality preserved:
  - S4 Monitor USB serial communication ✓
  - FTMS/BLE broadcasting ✓
  - ANT+ broadcasting ✓
  - ANT+ heart rate receiving ✓
  - Web interface on port 9001 ✓

### Migration Notes
For users upgrading from PiRowFlo:
1. The screen adapter is no longer supported
2. Use the web interface (port 9001) or command line instead
3. All other functionality remains the same
4. Installation is simpler and works on more platforms
