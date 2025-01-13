import os
import random
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.error import BadRequest

# Load environment variables
print("Loading environment variables...")
load_dotenv()

# Debug prints
print("Starting bot initialization...")
token = os.getenv('TELEGRAM_TOKEN')
spotify_id = os.getenv('SPOTIFY_CLIENT_ID')
spotify_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

print(f"Telegram Token exists: {'Yes' if token else 'No'}")
print(f"Spotify Client ID exists: {'Yes' if spotify_id else 'No'}")
print(f"Spotify Client Secret exists: {'Yes' if spotify_secret else 'No'}")

try:
    # Spotify API setup
    print("Setting up Spotify API...")
    spotify = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(
            client_id=spotify_id,
            client_secret=spotify_secret
        )
    )
    print("Spotify API setup completed successfully")
except Exception as e:
    print(f"Error setting up Spotify API: {str(e)}")
    raise

# Define popular genres
GENRES = [
    "pop", "rock", "hip hop", "jazz", "classical", 
    "electronic", "indie", "metal", "r&b", "country"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    print(f"Received /start command from user {update.effective_user.id}")
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
    
    try:
        # Try to answer the callback query first
        try:
            await query.answer()
        except BadRequest as e:
            if "Query is too old" in str(e):
                # If the query is too old, send a new message instead
                await query.message.reply_text(
                    "This button is too old to process. Please use /start to get fresh buttons."
                )
                return
            else:
                raise e
        
        genre = query.data
        print(f"Searching for {genre} tracks...")
        
        # Search for tracks in the selected genre
        results = spotify.search(q=f'genre:{genre}', type='track', limit=50)
        
        if not results['tracks']['items']:
            await query.message.reply_text(
                f"Sorry, no tracks found for {genre}. Try another genre!"
            )
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
        
        # Send a new message instead of editing
        await query.message.reply_text(
            text=message,
            reply_markup=reply_markup
        )
    
    except Exception as e:
        print(f"Error handling button press: {str(e)}")
        error_message = (
            "Sorry, something went wrong while processing your request.\n"
            "Please try again using /start command."
        )
        try:
            await query.message.reply_text(error_message)
        except Exception:
            print("Could not send error message")

def main():
    """Start the bot."""
    try:
        print("Creating Telegram bot application...")
        # Create the Application and pass it your bot's token
        application = Application.builder().token(token).build()

        print("Adding command handlers...")
        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button))

        print("Starting bot polling...")
        # Start the Bot
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        print(f"Error in main function: {str(e)}")
        raise

if __name__ == '__main__':
    print("Starting bot main function...")
    main() 