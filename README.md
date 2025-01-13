# Music Recommender Telegram Bot

A Telegram bot that recommends random songs based on user-selected genres using the Spotify API.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Local Development Setup](#local-development-setup)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running Locally](#running-locally)
- [Deployment](#deployment)
  - [AWS EC2 Deployment](#aws-ec2-deployment)
  - [Service Management](#service-management)
  - [Updating the Bot](#updating-the-bot)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Features
- Select from 10 popular music genres
- Get random song recommendations with direct Spotify links
- Easy-to-use interface with inline buttons
- Detailed song information including artist and album
- Automatic service recovery and restart
- Deployment ready for AWS EC2

## Prerequisites
- Python 3.7+
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Spotify Developer Account and API Credentials
- For deployment: AWS Account with EC2 access

## Local Development Setup

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/musicRecommenderBot.git
   cd musicRecommenderBot
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your API credentials:
   ```env
   TELEGRAM_TOKEN=your_telegram_token_here
   SPOTIFY_CLIENT_ID=your_spotify_client_id_here
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
   ```

### Running Locally
```bash
python bot.py
```

## Deployment

### AWS EC2 Deployment
1. Launch an EC2 instance with Ubuntu 24.04
2. Configure Security Groups:
   - Allow SSH (Port 22)
   - Allow HTTPS (Port 443)

3. Connect to your instance:
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

4. Run the setup script:
   ```bash
   wget https://raw.githubusercontent.com/YOUR_USERNAME/musicRecommenderBot/main/setup.sh
   chmod +x setup.sh
   ./setup.sh
   ```

5. Configure the bot:
   ```bash
   nano ~/musicRecommenderBot/.env
   ```

6. Start the service:
   ```bash
   sudo systemctl start telegram-bot
   ```

### Service Management
Monitor and control the bot service:
```bash
# Check status
sudo systemctl status telegram-bot

# View logs
sudo journalctl -u telegram-bot -f

# Start the bot
sudo systemctl start telegram-bot

# Stop the bot
sudo systemctl stop telegram-bot

# Restart the bot
sudo systemctl restart telegram-bot
```

### Updating the Bot
To update the deployed bot:
```bash
cd ~/musicRecommenderBot
sudo systemctl stop telegram-bot
git pull
sudo systemctl start telegram-bot
```

## Usage
1. Start a chat with your bot on Telegram
2. Send the `/start` command
3. Select a genre from the available buttons
4. Get a random song recommendation with a Spotify link
5. Select another genre to get more recommendations

## Troubleshooting
Common issues and solutions:

1. Bot not responding:
   ```bash
   # Check bot status
   sudo systemctl status telegram-bot
   # View error logs
   sudo journalctl -u telegram-bot -f
   ```

2. Service won't start:
   - Check .env file configuration
   - Verify API tokens
   - Check permissions: `sudo chown -R ubuntu:ubuntu ~/musicRecommenderBot`

3. Old callback queries:
   - Use `/start` to get fresh buttons
   - The bot automatically handles expired callbacks

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Technologies Used
- Python 3.7+
- python-telegram-bot
- Spotipy (Spotify API wrapper)
- python-dotenv
- systemd (for service management)
- AWS EC2 (for deployment) 