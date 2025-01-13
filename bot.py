import os
import random
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Load environment variables
load_dotenv()

# Spotify API setup
spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
    )
)

# Define popular genres
GENRES = [
    "pop", "rock", "hip hop", "jazz", "classical", 
    "electronic", "indie", "metal", "r&b", "country"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    keyboard = [
        [InlineKeyboardButton(genre.title(), callback_data=genre)]
        for genre in GENRES
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        'Welcome to the Music Recommender Bot! 🎵\n'
        'Please select a genre to get a random song recommendation:',
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses."""
    query = update.callback_query
    await query.answer()
    
    genre = query.data
    try:
        # Search for tracks in the selected genre
        results = spotify.search(q=f'genre:{genre}', type='track', limit=50)
        
        if not results['tracks']['items']:
            await query.edit_message_text(f"Sorry, no tracks found for {genre}. Try another genre!")
            return
        
        # Select a random track from the results
        track = random.choice(results['tracks']['items'])
        
        # Format the response
        artist_names = ', '.join(artist['name'] for artist in track['artists'])
        message = (
            f"🎵 Here's your {genre} recommendation:\n\n"
            f"🎼 Track: {track['name']}\n"
            f"👤 Artist(s): {artist_names}\n"
            f"💿 Album: {track['album']['name']}\n"
            f"🔗 Listen on Spotify: {track['external_urls']['spotify']}\n\n"
            f"Want another recommendation? Just select a genre!"
        )
        
        # Create keyboard for another recommendation
        keyboard = [
            [InlineKeyboardButton(g.title(), callback_data=g)]
            for g in GENRES
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=message,
            reply_markup=reply_markup
        )
    
    except Exception as e:
        await query.edit_message_text(f"An error occurred: {str(e)}")

def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token(os.getenv('TELEGRAM_TOKEN')).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    # Start the Bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 