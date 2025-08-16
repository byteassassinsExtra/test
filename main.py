#!/usr/bin/env python3
"""
Telegram Bot with Interactive Menu
Compatible with Python 3.13 and python-telegram-bot library
"""

import logging
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states for adding buttons
BUTTON_TEXT, BUTTON_TYPE, URL_INPUT, CALLBACK_INPUT = range(4)

# File to store dynamic buttons
BUTTONS_FILE = "dynamic_buttons.json"

# Bot token placeholder - replace with your actual bot token
BOT_TOKEN = "7054945394:AAGbjMWSwcH_MGQCoorLVBhBxF6tJd9KcQg"

# Shop URL placeholder - replace with your actual shop URL
SHOP_URL = "https://t.me/your_shop_channel"

# List of authorized admin chat IDs
# Replace with your actual chat ID to test the admin features
ADMINS = [
    1201917438,  # Example admin ID for HACKSAGE
]

# Payment methods message
PAYMENT_MESSAGE = "We acceps the following payment options:\n\n• Apple Pay\n• Zelle\n• Cash App (Bitcoin)\n• PayPal"

def is_admin(user_id: int) -> bool:
    """Checks if a user is an authorized admin."""
    return user_id in ADMINS

def load_buttons():
    """Load dynamic buttons from a JSON file."""
    try:
        with open(BUTTONS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_buttons(buttons):
    """Save dynamic buttons to a JSON file."""
    with open(BUTTONS_FILE, 'w') as f:
        json.dump(buttons, f, indent=4)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /start command by sending a welcome message with an inline keyboard menu.
    """
    try:
        welcome_message = (
            "🎉 Welcome to the HACKSAGE bot!\n\n"
            "Choose an option from the menu below to get started:"
        )

        # Create the initial keyboard
        keyboard = [
            [InlineKeyboardButton("🛒 View Shop", url=SHOP_URL)],
            [InlineKeyboardButton("💰 Payment Methods", callback_data="show_payments")]
        ]

        # Load dynamic buttons and add them to the keyboard
        dynamic_buttons = load_buttons()
        for btn in dynamic_buttons:
            if btn['type'] == 'url':
                keyboard.append([InlineKeyboardButton(btn['text'], url=btn['value'])])
            elif btn['type'] == 'text':
                keyboard.append([InlineKeyboardButton(btn['text'], callback_data=btn['value'])])

        # Add an Admin button if the user is an admin
        if is_admin(update.effective_user.id):
            keyboard.append([InlineKeyboardButton("⚙️ Admin Menu", callback_data="admin_menu")])

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            welcome_message,
            reply_markup=reply_markup
        )

        logger.info(f"Start command sent to user {update.effective_user.id}")

    except Exception as e:
        logger.error(f"Error in start_command: {e}")
        await update.message.reply_text(
            "Sorry, something went wrong. Please try again later."
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle button clicks from the inline keyboard.
    """
    try:
        query = update.callback_query
        await query.answer()

        data = query.data

        if data == "show_payments":
            await query.edit_message_text(text=PAYMENT_MESSAGE)
            logger.info(f"Payment methods shown to user {update.effective_user.id}")

        elif data == "admin_menu":
            await show_admin_menu(update, context)

        # Handle dynamic buttons
        else:
            dynamic_buttons = load_buttons()
            for btn in dynamic_buttons:
                if btn['value'] == data:
                    await query.edit_message_text(text=btn['text'])
                    logger.info(f"Dynamic text button '{btn['text']}' clicked by user {update.effective_user.id}")
                    return

    except Exception as e:
        logger.error(f"Error in button_callback: {e}")
        try:
            await query.answer("Something went wrong. Please try again.")
        except:
            pass

async def show_admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays the admin menu with options for adding buttons."""
    if not is_admin(update.effective_user.id):
        await update.effective_message.reply_text("You are not authorized to view the admin menu.")
        return

    admin_keyboard = [
        [InlineKeyboardButton("➕ Add New Button", callback_data="add_button")],
    ]
    reply_markup = InlineKeyboardMarkup(admin_keyboard)

    await update.effective_message.edit_text(
        "🛠️ Admin Menu\n\nChoose an option:",
        reply_markup=reply_markup
    )
    logger.info(f"Admin menu shown to user {update.effective_user.id}")

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Allows an admin to add another admin."""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("You are not authorized to use this command.")
        return

    try:
        new_admin_id = int(context.args[0])
        if new_admin_id not in ADMINS:
            ADMINS.append(new_admin_id)
            await update.message.reply_text(f"User with chat ID {new_admin_id} has been added as an admin.")
            logger.info(f"New admin added: {new_admin_id} by user {update.effective_user.id}")
        else:
            await update.message.reply_text(f"User with chat ID {new_admin_id} is already an admin.")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /admin <chat_id>")

# --- Conversation handlers for adding buttons ---
async def add_button_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation to add a new button."""
    if not is_admin(update.effective_user.id):
        await update.effective_message.reply_text("You are not authorized to add buttons.")
        return ConversationHandler.END

    await update.effective_message.reply_text(
        "Please provide the text for the new button. "
        "Or type /cancel to stop."
    )
    return BUTTON_TEXT

async def get_button_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the button text and asks for the button type."""
    button_text = update.message.text
    context.user_data['button_text'] = button_text
    
    await update.message.reply_text(
        f"The button text will be '{button_text}'.\n\n"
        "Now, what kind of button is it?\n"
        "1. Redirect URL (e.g., website link)\n"
        "2. Plain Text (shows a message when clicked)\n"
        "Type 'url' or 'text'. Or type /cancel to stop."
    )
    return BUTTON_TYPE

async def get_button_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the button type and asks for the button value (URL or text)."""
    button_type = update.message.text.lower()
    if button_type not in ["url", "text"]:
        await update.message.reply_text("Invalid type. Please type 'url' or 'text'.")
        return BUTTON_TYPE
    
    context.user_data['button_type'] = button_type
    
    if button_type == 'url':
        await update.message.reply_text("Please enter the full URL for the button (e.g., https://example.com).")
        return URL_INPUT
    else:  # 'text'
        await update.message.reply_text("Please enter the plain text message to be displayed when the button is clicked.")
        return CALLBACK_INPUT

async def get_button_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Adds the new URL button and ends the conversation."""
    button_url = update.message.text
    new_button = {
        'text': context.user_data['button_text'],
        'type': 'url',
        'value': button_url
    }
    
    dynamic_buttons = load_buttons()
    dynamic_buttons.append(new_button)
    save_buttons(dynamic_buttons)
    
    await update.message.reply_text(f"✅ New button '{new_button['text']}' with URL added successfully! Use /start to see it.")
    logger.info(f"New URL button added: {new_button} by user {update.effective_user.id}")
    
    return ConversationHandler.END

async def get_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Adds the new text button and ends the conversation."""
    button_text_value = update.message.text
    new_button = {
        'text': context.user_data['button_text'],
        'type': 'text',
        'value': button_text_value
    }
    
    dynamic_buttons = load_buttons()
    dynamic_buttons.append(new_button)
    save_buttons(dynamic_buttons)
    
    await update.message.reply_text(f"✅ New button '{new_button['text']}' with plain text added successfully! Use /start to see it.")
    logger.info(f"New text button added: {new_button} by user {update.effective_user.id}")
    
    return ConversationHandler.END

async def cancel_add_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels the conversation to add a new button."""
    await update.message.reply_text("🚫 Operation canceled.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle errors that occur during bot operation.
    """
    logger.error(f"Update {update} caused error {context.error}")

def main() -> None:
    """
    Main function to set up and run the bot.
    """
    try:
        if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            logger.error("Please replace BOT_TOKEN with your actual bot token!")
            print("❌ Error: Please replace BOT_TOKEN with your actual bot token!")
            return

        application = Application.builder().token(BOT_TOKEN).build()

        # Add conversation handler for adding buttons
        add_button_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(add_button_start, pattern="^add_button$")],
            states={
                BUTTON_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_button_text)],
                BUTTON_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_button_type)],
                URL_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_button_url)],
                CALLBACK_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_button_callback)],
            },
            fallbacks=[CommandHandler("cancel", cancel_add_button)],
        )

        # Add handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("admin", admin_command))
        application.add_handler(CallbackQueryHandler(button_callback))
        application.add_handler(add_button_handler)

        # Add error handler
        application.add_error_handler(error_handler)

        logger.info("Bot is starting...")
        print("🚀 Bot is starting...")
        print("💡 Remember to set your actual BOT_TOKEN and admin chat ID!")
        print("🔄 Bot is running... Press Ctrl+C to stop.")

        application.run_polling(drop_pending_updates=True)

    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        print(f"❌ Failed to start bot: {e}")

if __name__ == '__main__':
    main()
