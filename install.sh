#!/bin/bash
# RowFlo Installation Script
# Device-neutral fork - works on any Linux system with Bluetooth support

set -e  # Exit the script if any command fails

echo " "
echo "=========================================="
echo "  RowFlo for WaterRower"
echo "  Device-Neutral Installation"
echo "=========================================="
echo " "

# Check if running as root
if [ "$EUID" -eq 0 ]; then
   echo "Please do not run this script as root/sudo"
   echo "Run it as your regular user - it will prompt for sudo when needed"
   exit 1
fi

CURRENT_USER=$(whoami)
REPO_DIR=$(cd $(dirname $0) > /dev/null 2>&1; pwd -P)

echo "Installing for user: $CURRENT_USER"
echo "Installation directory: $REPO_DIR"
echo " "

echo "-------------------------------------------------------------"
echo "Updating package list..."
echo "-------------------------------------------------------------"
sudo apt-get update

echo " "
echo "-------------------------------------------------------------"
echo "Installing required system packages..."
echo "-------------------------------------------------------------"
sudo apt-get install -y \
    python3 \
    python3-gi \
    python3-gi-cairo \
    gir1.2-gtk-3.0 \
    python3-pip \
    python3-venv \
    libdbus-1-dev \
    libglib2.0-dev \
    libgirepository1.0-dev \
    libcairo2-dev \
    bluetooth \
    bluez

echo " "
echo "-------------------------------------------------------------"
echo "Creating Python virtual environment..."
echo "-------------------------------------------------------------"
python3 -m venv venv

echo " "
echo "-------------------------------------------------------------"
echo "Installing Python dependencies..."
echo "-------------------------------------------------------------"
venv/bin/pip install --upgrade pip
venv/bin/pip install --break-system-packages -r requirements.txt

echo " "
echo "-------------------------------------------------------------"
echo "Adding user to required groups..."
echo "-------------------------------------------------------------"
sudo usermod -a -G bluetooth "$CURRENT_USER"
sudo usermod -a -G dialout "$CURRENT_USER"

echo " "
echo "-------------------------------------------------------------"
echo "Creating logging configuration..."
echo "-------------------------------------------------------------"
cat > src/logging.conf << 'EOF'
[loggers]
keys=root

[handlers]
keys=consoleHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=INFO
handlers=consoleHandler

[handler_consoleHandler]
class=StreamHandler
level=INFO
formatter=simpleFormatter
args=(sys.stdout,)

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
EOF

echo " "
echo "-------------------------------------------------------------"
echo "Creating systemd service..."
echo "-------------------------------------------------------------"
sudo tee /etc/systemd/system/rowflo.service > /dev/null << EOF
[Unit]
Description=RowFlo WaterRower BLE Service
After=network.target bluetooth.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$REPO_DIR
ExecStart=$REPO_DIR/venv/bin/python3 $REPO_DIR/src/waterrowerthreads.py -i s4 -b
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo " "
echo "-------------------------------------------------------------"
echo "Enabling and starting RowFlo service..."
echo "-------------------------------------------------------------"
sudo systemctl daemon-reload
sudo systemctl enable rowflo

echo " "
echo "-------------------------------------------------------------"
echo "Setting Bluetooth device name to 'RowFlo'..."
echo "-------------------------------------------------------------"
echo "PRETTY_HOSTNAME=RowFlo" | sudo tee /etc/machine-info > /dev/null
echo " "
echo "-------------------------------------------------------------"
echo "Configuring Bluetooth for pairing-free operation..."
echo "-------------------------------------------------------------"

# Unblock Bluetooth (in case it's blocked)
sudo rfkill unblock bluetooth

# Start Bluetooth service
sudo systemctl start bluetooth
sudo systemctl enable bluetooth

# Wait for Bluetooth to be ready
sleep 2

# Configure Bluetooth adapter for pairing-free operation
sudo bluetoothctl <<EOF
power on
discoverable on
pairable on
agent NoInputNoOutput
default-agent
quit
EOF

echo "Bluetooth configured successfully"
echo " "
echo "=============================================="
echo "  Installation Complete!"
echo "=============================================="
echo " "
echo "IMPORTANT: You must log out and log back in"
echo "for group changes to take effect."
echo " "
echo "After logging back in, RowFlo will start automatically."
echo " "
echo "Useful commands:"
echo "  sudo systemctl status rowflo    # Check service status"
echo "  sudo systemctl restart rowflo   # Restart service"
echo "  sudo journalctl -u rowflo -f    # View live logs"
echo " "
echo "Or run manually for testing:"
echo "  $REPO_DIR/venv/bin/python3 $REPO_DIR/src/waterrowerthreads.py -i s4 -b"
echo " "
