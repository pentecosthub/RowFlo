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

echo "Installing for user: $CURRENT_USER"
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
venv/bin/pip install -r requirements.txt

echo " "
echo "-------------------------------------------------------------"
echo "Adding user to required groups..."
echo "-------------------------------------------------------------"
sudo usermod -a -G bluetooth "$CURRENT_USER"
sudo usermod -a -G dialout "$CURRENT_USER"

echo " "
echo "-------------------------------------------------------------"
echo "Setting Bluetooth device name to 'RowFlo'..."
echo "-------------------------------------------------------------"
echo "PRETTY_HOSTNAME=RowFlo" | sudo tee /etc/machine-info > /dev/null

echo " "
echo "-------------------------------------------------------------"
echo "Configuring web interface on port 9001..."
echo "-------------------------------------------------------------"
export repo_dir=$(cd $(dirname $0) > /dev/null 2>&1; pwd -P)
export python3_path="$repo_dir/venv/bin/python3"
export supervisord_path=$(which supervisord)
export supervisorctl_path=$(which supervisorctl)

cp services/supervisord.conf.orig services/supervisord.conf
sed -i 's@#PYTHON3#@'"$python3_path"'@g' services/supervisord.conf
sed -i 's@#REPO_DIR#@'"$repo_dir"'@g' services/supervisord.conf
sed -i 's@#USER#@'"$CURRENT_USER"'@g' services/supervisord.conf

echo " "
echo "-------------------------------------------------------------"
echo "Setting up systemd service for supervisord..."
echo "-------------------------------------------------------------"
cp services/supervisord.service services/supervisord.service.tmp
sed -i 's@#REPO_DIR#@'"$repo_dir"'@g' services/supervisord.service.tmp
sed -i 's@#SUPERVISORD_PATH#@'"$supervisord_path"'@g' services/supervisord.service.tmp
sed -i 's@#SUPERVISORCTL_PATH#@'"$supervisorctl_path"'@g' services/supervisord.service.tmp
sudo mv services/supervisord.service.tmp /etc/systemd/system/supervisord.service
sudo chown root:root /etc/systemd/system/supervisord.service
sudo chmod 644 /etc/systemd/system/supervisord.service
sudo systemctl enable supervisord

echo " "
echo "-------------------------------------------------------------"
echo "Updating logging configuration..."
echo "-------------------------------------------------------------"
cp src/logging.conf.orig src/logging.conf
sed -i 's@#REPO_DIR#@'"$repo_dir"'@g' src/logging.conf

echo " "
echo "-------------------------------------------------------------"
echo "Cleaning up temporary files..."
echo "-------------------------------------------------------------"
sudo rm -f /tmp/rowflo*
sudo rm -f /tmp/supervisord.log

echo " "
echo "=============================================="
echo "  Installation Complete!"
echo "=============================================="
echo " "
echo "IMPORTANT: You must log out and log back in"
echo "for group changes to take effect."
echo " "
echo "After logging back in, start RowFlo with:"
echo "  sudo systemctl start supervisord"
echo " "
echo "Access web interface at:"
echo "  http://$(hostname -I | awk '{print $1}'):9001"
echo " "
echo "Or run manually:"
echo "  venv/bin/python3 src/waterrowerthreads.py -i s4 -b -a"
echo " "

exit 0
