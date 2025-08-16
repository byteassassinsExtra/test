#!/usr/bin/env python3
"""
Telegram Bot with Interactive Menu
Compatible with Python 3.13 and python-telegram-bot library
"""

import logging
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

# Shop URL placeholder - replace with your actual shop URL
SHOP_URL = "https://t.me/your_shop_channel"

# Payment methods message
PAYMENT_MESSAGE = "We offer the following payment options:\n\n• Apple Pay\n• Zelle\n• Cash App (Bitcoin)\n• PayPal"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /start command by sending a welcome message with an inline keyboard menu.
    """
    try:
        welcome_message = (
            "🎉 Welcome to the HACKSAGE bot!\n\n"
            "Choose an option from the menu below to get started:"
        )

        # Create inline keyboard with two new buttons
        # The 'View Shop' button has a URL
        # The 'Payment Methods' button has a callback_data
        keyboard = [
            [InlineKeyboardButton("🛒 View Shop", url=SHOP_URL)],
            [InlineKeyboardButton("💰 Payment Methods", callback_data="show_payments")]
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

        # Always answer the callback query to remove the loading spinner on the button
        await query.answer()

        # Check which button was clicked based on the callback_data
        if query.data == "show_payments":
            # Edit the message to show the payment options
            await query.edit_message_text(text=PAYMENT_MESSAGE)
            logger.info(f"Payment methods shown to user {update.effective_user.id}")

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

        # Create the Application
        application = Application.builder().token(BOT_TOKEN).build()

        # Add handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CallbackQueryHandler(button_callback))

        # Add error handler
        application.add_error_handler(error_handler)

        # Log startup
        logger.info("Bot is starting...")
        print("🚀 Bot is starting...")
        print(f"🛒 Shop URL set to: {SHOP_URL}")
        print("💡 Make sure to replace BOT_TOKEN and SHOP_URL with actual values!")
        print("🔄 Bot is running... Press Ctrl+C to stop.")

        # Run the bot
        application.run_polling(drop_pending_updates=True)

    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        print(f"❌ Failed to start bot: {e}")

if __name__ == '__main__':
    main()
