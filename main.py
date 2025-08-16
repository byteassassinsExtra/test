#!/usr/bin/env python3
"""
Telegram Bot with Interactive Menu
Compatible with Python 3.13 and python-telegram-bot library
"""

import logging
import pytz
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token placeholder - replace with your actual bot token
BOT_TOKEN = "7054945394:AAGbjMWSwcH_MGQCoorLVBhBxF6tJd9KcQg"

# Channel URL placeholder - replace with your actual channel URL
CHANNEL_URL = "https://t.me/your_channel_name"

CHANNEL_URL2 = "https://www.instagram.com/hacksagex/"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /start command by sending welcome message with inline keyboard menu.
    """
    try:
        welcome_message = (
            "🎉 Welcome to our bot!\n\n"
            "Choose an option from the menu below to get started:"
        )
        
        # Create inline keyboard with two buttons
        keyboard = [
            [InlineKeyboardButton("📦 Join our channel to see products", url=CHANNEL_URL)],
            [InlineKeyboardButton("⭐️ Reviews & Touch Down", url=CHANNEL_URL2)]
        ]
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
        
        # Acknowledge the callback query
        await query.answer()
        
        if query.data == "reviews":
            # Update the message when reviews button is clicked
            thank_you_message = (
                "⭐️ Thank you for your interest in our reviews! "
                "We appreciate you! ⭐️\n\n"
                "Your feedback means the world to us!"
            )
            
            await query.edit_message_text(
                text=thank_you_message
            )
            
            logger.info(f"Reviews button clicked by user {update.effective_user.id}")
        
    except Exception as e:
        logger.error(f"Error in button_callback: {e}")
        try:
            await query.answer("Something went wrong. Please try again.")
        except:
            pass

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
        # Validate bot token
        if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            logger.error("Please replace BOT_TOKEN with your actual bot token!")
            print("❌ Error: Please replace BOT_TOKEN with your actual bot token!")
            return
        
        # Create the Application with timezone support
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CallbackQueryHandler(button_callback))
        
        # Add error handler
        application.add_error_handler(error_handler)
        
        # Log startup
        logger.info("Bot is starting...")
        print("🚀 Bot is starting...")
        print(f"📱 Channel URL set to: {CHANNEL_URL}")
        print("💡 Make sure to replace BOT_TOKEN and CHANNEL_URL with actual values!")
        print("🔄 Bot is running... Press Ctrl+C to stop.")
        
        # Run the bot
        application.run_polling(drop_pending_updates=True)
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        print(f"❌ Failed to start bot: {e}")

if __name__ == '__main__':
    main()
    
