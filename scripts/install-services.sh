#!/bin/bash
#
# Install systemd service files for running on startup.


SYSTEMD_FOLDER=/etc/systemd/system

# Copy service config
sudo cp aplay.service $SYSTEMD_FOLDER
sudo cp mjpg_streamer.service $SYSTEMD_FOLDER

# Enable service
sudo systemctl enable aplay
sudo systemctl enable mjpg_streamer

# Copy config
sudo cp asound.conf /etc
sudo cp config.txt /boot
