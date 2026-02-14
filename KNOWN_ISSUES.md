# Known Issues

## Bluetooth Pairing Rejections

**Symptoms:** Apps can discover RowFlo but get "pairing rejected" errors

**Workaround:**
```bash
sudo rfkill unblock bluetooth
sudo bluetoothctl
power on
discoverable on
pairable on
agent NoInputNoOutput
default-agent
quit
```

**Status:** Investigating automatic configuration in install.sh

## Compatibility

### Multiple Bluetooth Adapters

Using multiple Bluetooth adapters simultaneously (internal + USB) can cause system instability on some hardware.

**Solution:** Use only one Bluetooth adapter at a time
- Disable internal Bluetooth in BIOS and use USB adapter, OR
- Use only internal Bluetooth (remove USB adapter)

**Tested Working:**
- Dell Optiplex 3050: USB Bluetooth adapter (internal disabled in BIOS)
- Raspberry Pi 3B: Internal Bluetooth

### WaterRower S4 USB Detection

On some systems, S4 monitor may require specific USB ports for reliable detection.

**Symptoms:** "port not found" warnings in logs even when S4 is plugged in

**Workaround:** Try different USB ports, especially USB 2.0 ports

## Reporting Issues

Report issues at: https://github.com/pentecosthub/RowFlo/issues

Include:
- OS version and hardware platform
- Output of `sudo journalctl -u rowflo -n 50`
- Output of `hciconfig -a`
- Steps to reproduce
