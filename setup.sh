#!/bin/bash

# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python, pip, and git
sudo apt install python3-pip python3-venv git -y

# Remove existing directory if it exists
rm -rf ~/musicRecommenderBot

# Clone the repository
git clone https://github.com/apih99/musicRecommenderBot.git ~/musicRecommenderBot
cd ~/musicRecommenderBot

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install -r requirements.txt

# Create .env file (you'll need to edit this with your actual tokens)
cp .env.example .env

# Set correct permissions
sudo chown -R ubuntu:ubuntu ~/musicRecommenderBot
chmod +x ~/musicRecommenderBot/bot.py

# Copy service file to systemd
sudo cp telegram-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot

# Show debug information
echo "Debug information:"
echo "===================="
ls -la ~/musicRecommenderBot
echo "===================="
ls -la ~/musicRecommenderBot/venv/bin
echo "===================="
cat /etc/systemd/system/telegram-bot.service
echo "===================="

# Prompt user to edit .env file
echo "Please edit the .env file with your API tokens:"
echo "nano ~/musicRecommenderBot/.env"
echo ""
echo "After editing .env, start the service with:"
echo "sudo systemctl start telegram-bot"
echo ""
echo "To check status:"
echo "sudo systemctl status telegram-bot"
echo ""
echo "To view logs:"
echo "sudo journalctl -u telegram-bot -f" 