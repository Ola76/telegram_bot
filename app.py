import os
import datetime
import random
from dotenv import load_dotenv
from typing import Final
import logging  # Import the logging module
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CallbackContext

# Load environment variables from .env file
load_dotenv()

# Securely fetch your tokens and keys from the environment variable
TOKEN: Final = os.environ.get('TOKEN')
BOT_USERNAME: Final = os.environ.get('BOT_USERNAME')

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ---------------------------------------------------HOME-------------------------------------------------------------------

#handling the Home commands
async def home_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_name = "WhizBot, Your Wizardly Assistant"
    home_text = (
        f"🌟 **Greetings, Adventurer! I am {bot_name}!** 🌟\n\n"
        f"Embark on a magical journey with me, your wizardly assistant. "
        f"Type /help to discover the enchanted commands and let the magic unfold. "
        f"Whether you seek knowledge or simply wish to chat, I'm here for you!\n\n"
        f"Cast a spell with {bot_name}! 🧙✨"
    )
    update.message.reply_text(home_text)

# --------------------------------------------------------HELP-------------------------------------------------------------------

# Help descriptions
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🌟 **Welcome to the News Bot!** 🌟\n\n"
        "Here are some commands to get you started:\n\n"
        "/home - Welcome message and basic bot instructions.\n"
        "/help - Shows this help message detailing command usage.\n"
        "/custom - Sends a custom message.\n"
        "/game - Fetches and displays the latest news.\n"
        "/list - Displays your shopping list. You can tick off items.\n"
        "/dataset - Allows you to upload a CSV dataset.\n\n"
        "Feel free to explore and use these commands!"
    )
    update.message.reply_text(help_text)

# ----------------------------------------------------------CUSTOM----------------------------------------------------------------

# Custom command chat
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    under_construction_text = (
        "🚧 **Under Construction!** 🚧\n\n"
        "Sorry, the custom feature is still in development. "
        "We're working hard to bring you exciting new features. "
        "Stay tuned for updates! 😊"
    )
    await update.message.reply_text(under_construction_text)

# --------------------------------------------------------RESPONSE CHAT--------------------------------------------------------------

# Handles response 
def handle_response(text: str) -> str:
    processed = text.lower()

    # Time-based greeting
    current_time = datetime.datetime.now().time()
    if current_time < datetime.time(12, 0):
        greeting = 'Good morning'
    elif current_time < datetime.time(17, 0):
        greeting = 'Good afternoon'
    else:
        greeting = 'Good evening'

    if any(keyword in processed for keyword in ['hi', 'hello', 'hey']):
        return f'{greeting}! How can I assist you today? 😊'

    if 'how are you' in processed:
        return "I'm just a bot, but I'm doing well! How can I help you?"

    if 'who are you' in processed:
        return "I am your friendly bot here to assist you with various tasks!"

    if 'thank you' in processed:
        return "You're welcome! If you have more requests, feel free to ask."

    if 'help' in processed or 'need assistance' in processed:
        return "Certainly! I'm here to help. What do you need assistance with? You can ask about the game, your shopping list, or use commands like /custom or /dataset."

    if 'what can you do' in processed:
        return "I can play a game with you, manage your shopping list, and more! Feel free to explore the commands."

    if 'how do you work' in processed:
        return "I work by responding to specific commands. You can try commands like /game, /shoppinglist, or /custom to see what I can do."

    if 'recommend' in processed:
        return "Sure! What are you looking for a recommendation on? A game, a product, or something else?"

    if 'game' in processed:
        return f'{greeting}! Let\'s have a chat about the game. What aspect of the game would you like to discuss? Strategy, rules, or maybe a challenge?'

    if any(keyword in processed for keyword in ['please', 'kindly']):
        return "Thank you for your polite request! How may I assist you? 😊"

    unrecognized_response = [
        "Oops! It seems like I didn't catch that. Could you please rephrase your question?",
        "I'm sorry, I didn't quite get that. Could you try asking in a different way?",
        "My circuits might be a bit tangled! Can you help me understand your question better?",
    ]
    return random.choice(unrecognized_response)

# ----------------------------------------------------------------GAME FEATURE-------------------------------------------------------------------

# Guess the number game one-run
def game_command(update: Update, context: CallbackContext):
    difficulty_text = (
        "Let's play a game! Choose a difficulty level:\n"
        "/game easy - Guess a number between 1 and 50 (easy)\n"
        "/game medium - Guess a number between 1 and 100 (medium)\n"
        "/game hard - Guess a number between 1 and 200 (hard)"
    )
    update.message.reply_text(difficulty_text)

def start_game(update: Update, context: CallbackContext, difficulty: str, max_range: int):
    # Generate a random number based on the difficulty level
    secret_number = random.randint(1, max_range)

    # Store the secret number and the maximum attempts in the user's context for later reference
    context.user_data['secret_number'] = secret_number
    context.user_data['max_attempts'] = 5  # You can adjust the number of attempts as needed

    game_text = (
        f"Great choice! I'm thinking of a number between 1 and {max_range}. "
        "Try to guess the correct number by using the /guess command followed by your guess. "
        f"For example, type /guess 50 to guess the number 50."
    )
    update.message.reply_text(game_text)

# Add a handler for the /guess command
def guess_command(update: Update, context: CallbackContext):
    user_guess = int(context.args[0]) if context.args and context.args[0] else None

    if user_guess is None:
        update.message.reply_text("Please provide a number as your guess. Example: /guess 50")
        return

    # Retrieve the secret number from the user's context
    secret_number = context.user_data.get('secret_number')

    if secret_number is None:
        update.message.reply_text("Oops! Something went wrong. Let's start the game again with /game.")
        return

    if user_guess == secret_number:
        update.message.reply_text("Congratulations! You guessed the correct number. 🎉")
        # Clear the secret number from the user's context
        del context.user_data['secret_number']
    elif user_guess < secret_number:
        update.message.reply_text("Too low! Try a higher number.")
    else:
        update.message.reply_text("Too high! Try a lower number.")

# ----------------------------------------------------------------LIST FEATURE-------------------------------------------------------------------

def shopping_list_command(update: Update, context: CallbackContext):
    update.message.reply_text("Here's your shopping list. You can tick off items.")
    
# --------------------------------------------------------------------DATASET FEATURE--------------------------------------------------------------------

def dataset_command(update: Update, context: CallbackContext):
    update.message.reply_text("Please upload a CSV dataset.")

# ----------------------------------------------------------------------MESSAGE HANDLER--------------------------------------------------------------------
    
# Comment
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    logger.info(f'User ({update.message.chat.id}) in {message_type}: "{text}"') # Logs the chat chat type, Group/private

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    
    logger.info('Bot: ' + response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f'Update {update} caused error {context.error}')

# -------------------------------------------------------------------------APP POLLING--------------------------------------------------------------------------

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('home', home_command))
    app.add_handler(CommandHandler('list', shopping_list_command))  # Updated to use '/list' instead of '/shoppinglist'
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('dataset', dataset_command))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    # Add a handler for the /game command with difficulty levels
    app.add_handler(CommandHandler('game', game_command))
    app.add_handler(CommandHandler('easy', lambda update, context: start_game(update, context, 'easy', 50)))
    app.add_handler(CommandHandler('medium', lambda update, context: start_game(update, context, 'medium', 100)))
    app.add_handler(CommandHandler('hard', lambda update, context: start_game(update, context, 'hard', 200)))
    app.add_error_handler(error)

    logger.info('Bot is polling...')
    app.run_polling(poll_interval=3)