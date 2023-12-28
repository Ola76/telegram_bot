import os
import datetime
import random
from dotenv import load_dotenv
from typing import Final, List
import logging  # Import the logging module
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

# Load environment variables from .env file
load_dotenv()

# Securely fetch your tokens and keys from the environment variable
TOKEN: Final = os.environ.get('TOKEN')
BOT_USERNAME: Final = os.environ.get('BOT_USERNAME')

# Check if the token is provided
if TOKEN is None:
    raise ValueError("Telegram token not found. Make sure to set it in the .env file.")

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
    await update.message.reply_text(home_text)

# --------------------------------------------------------HELP-------------------------------------------------------------------

# Help descriptions
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🌟 **Welcome to the News Bot!** 🌟\n\n"
        "Here are some commands to get you started:\n\n"
        "/home - Welcome message and basic bot instructions.\n"
        "/help - Shows this help message detailing command usage.\n"
        "/custom - Sends a custom message.\n"
        "/game - Initiates a number-guessing game.\n"
        "/list - Manages your shopping list. You can add, view, and mark items as completed.\n"
        "  - Use /additem [item] to add an item to the list.\n"
        "  - Use /list to view your current shopping list.\n"
        "  - Use /tickoff [item] to mark an item as completed.\n"
        "/dataset - Allows you to upload a CSV dataset.\n\n"
        "Feel free to explore and use these commands!"
    )
    await update.message.reply_text(help_text)

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

    if any(keyword in processed for keyword in ['please', 'kindly']):
        return "Thank you for your polite request! How may I assist you? 😊"

    unrecognized_response = [
        "Oops! It looks like I missed that. Could you kindly rephrase your question?",
        "I apologize; I didn't fully grasp that. Could you try phrasing it differently?",
        "My circuits might be a bit confused! Can you provide more details for better understanding?"
    ]
    return random.choice(unrecognized_response)

# ----------------------------------------------------------------GAME FEATURE-------------------------------------------------------------------

# Guess the number game one-run
async def game_command(update: Update, context: CallbackContext):
    logger.info("Game command triggered.")
    difficulty_text = (
        "Let's play a game! Choose a difficulty level:\n"
        "/game easy - Guess a number between 1 and 50 (easy)\n"
        "/game medium - Guess a number between 1 and 100 (medium)\n"
        "/game hard - Guess a number between 1 and 200 (hard)"
    )
    await update.message.reply_text(difficulty_text) 

# ----------------------------------------------------------------LIST FEATURE-------------------------------------------------------------------

# Reusable function to get the shopping list from user_data
def get_shopping_list(context: CallbackContext) -> List[str]:
    return context.user_data.setdefault('shopping_list', [])

# Add a handler for the /viewlist command
def view_list_command(update: Update, context: CallbackContext):
    shopping_list = get_shopping_list(context)

    if not shopping_list:
        update.message.reply_text("Your shopping list is empty. Start adding items with /additem.")
    else:
        list_text = "Your shopping list:\n" + "\n".join([f" - {item}" for item in shopping_list])
        update.message.reply_text(list_text)
        update.message.reply_text("Tap on the buttons below to manage your list:",
                                reply_markup=create_shopping_list_buttons())

# Add a handler for the /additem command
def add_item_command(update: Update, context: CallbackContext):
    item = " ".join(context.args)

    if not item:
        update.message.reply_text("Please provide an item to add to the shopping list. Example: /additem eggs")
    else:
        shopping_list = get_shopping_list(context)
        shopping_list.append(item)

        update.message.reply_text(f"Added '{item}' to your shopping list. View your list with /viewlist.",
                                reply_markup=create_shopping_list_buttons())

# Improve user feedback
def tick_off_command(update: Update, context: CallbackContext):
    item = " ".join(context.args)

    if not item:
        update.message.reply_text("Please provide an item to mark as completed. Example: /tickoff eggs")
    else:
        shopping_list = get_shopping_list(context)

        if item in shopping_list:
            shopping_list.remove(item)
            remaining_items = len(shopping_list)
            update.message.reply_text(f"Marked '{item}' as completed. {remaining_items} items remaining. View your updated list with /list.",
                                    reply_markup=create_shopping_list_buttons())
        else:
            update.message.reply_text(f"Item '{item}' not found in your shopping list.")

# Add emojis to inline keyboard buttons
def create_shopping_list_buttons():
    buttons = [
        [InlineKeyboardButton("➕ Add Item", callback_data="additem")],
        [InlineKeyboardButton("✔️ Mark Completed", callback_data="markcompleted")]
    ]
    return InlineKeyboardMarkup(buttons)

# Handler for button clicks
def button_click_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "additem":
        update.message.reply_text("Use /additem [item] to add an item to the shopping list. Example: /additem eggs")
    elif query.data == "markcompleted":
        update.message.reply_text("Use /tickoff [item] to mark an item as completed. Example: /tickoff eggs")
    
# --------------------------------------------------------------------DATASET FEATURE--------------------------------------------------------------------

def dataset_command(update: Update, context: CallbackContext):
    update.message.reply_text("Please upload a CSV dataset.")

# ----------------------------------------------------------------------MESSAGE HANDLER--------------------------------------------------------------------
    
# Handle messages
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
    app.add_handler(CommandHandler('list', view_list_command))  # Using '/list' instead of '/shoppinglist'
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('dataset', dataset_command))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    # Add a handler for the /game command with difficulty levels
    app.add_handler(CommandHandler('game', game_command))
    app.add_error_handler(error)

    logger.info('Bot is polling...')
    app.run_polling(poll_interval=3)