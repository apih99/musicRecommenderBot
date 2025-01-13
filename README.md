# Music Recommender Telegram Bot

A Telegram bot that recommends random songs based on user-selected genres using the Spotify API.

## Features

- Select from 10 popular music genres
- Get random song recommendations with direct Spotify links
- Easy-to-use interface with inline buttons
- Detailed song information including artist and album

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your API keys:
   - Create a Telegram bot through [BotFather](https://t.me/botfather) and get the token
   - Create a Spotify Developer account and get your [API credentials](https://developer.spotify.com/dashboard)
   - Copy `.env.example` to `.env` and fill in your API keys:
     ```
     TELEGRAM_TOKEN=your_telegram_token_here
     SPOTIFY_CLIENT_ID=your_spotify_client_id_here
     SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
     ```

4. Run the bot:
   ```bash
   python bot.py
   ```

## Usage

1. Start a chat with your bot on Telegram
2. Send the `/start` command
3. Select a genre from the available buttons
4. Get a random song recommendation with a Spotify link
5. Select another genre to get more recommendations

## Technologies Used

- Python 3.7+
- python-telegram-bot
- Spotipy (Spotify API wrapper)
- python-dotenv 