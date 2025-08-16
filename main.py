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
    MessageHandler,
    ContextTypes,
    filters,
    ConversationHandler,
)

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

# Admin chat ID for anonymous chat support. Replace with your actual chat ID.
ADMIN_CHAT_ID = 1201917438

# File to store banned user IDs. This provides basic persistence.
BANNED_USERS_FILE = "banned_users.json"

# Conversation states for the chat support feature
CHAT_SUPPORT = range(1)

# Payment methods message
PAYMENT_MESSAGE = "We offer the following payment options:\n\n• Apple Pay\n• Zelle\n• Cash App (Bitcoin)\n• PayPal"

def load_banned_users() -> list:
    """Loads banned user IDs from a file."""
    try:
        with open(BANNED_USERS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_banned_users(banned_users: list):
    """Saves banned user IDs to a file."""
    with open(BANNED_USERS_FILE, 'w') as f:
        json.dump(banned_users, f)

def is_banned(user_id: int) -> bool:
    """Checks if a user is in the banned list."""
    return user_id in load_banned_users()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /start command by sending a welcome message with an inline keyboard menu.
    """
    try:
        welcome_message = (
            "🎉 Welcome to the HACKSAGE bot!\n\n"
            "Choose an option from the menu below to get started:"
        )

        # Create the initial keyboard with fixed buttons
        keyboard = [
            [InlineKeyboardButton("🛒 View Shop", url=SHOP_URL)],
            [InlineKeyboardButton("💰 Payment Methods", callback_data="show_payments")],
            [InlineKeyboardButton("💬 Chat Support", callback_data="start_chat_support")],
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
        await query.answer()

        if query.data == "show_payments":
            await query.edit_message_text(text=PAYMENT_MESSAGE)
            logger.info(f"Payment methods shown to user {update.effective_user.id}")

    except Exception as e:
        logger.error(f"Error in button_callback: {e}")
        try:
            await query.answer("Something went wrong. Please try again.")
        except:
            pass

async def start_chat_support(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Starts the conversation for chat support.
    """
    user_id = update.effective_user.id
    if is_banned(user_id):
        await update.effective_message.reply_text(
            "You are currently banned from using chat support."
        )
        return ConversationHandler.END

    await update.effective_message.reply_text(
        "You are now connected to chat support. Please type your message.\n"
        "To end the chat, type /endchat."
    )
    
    # Send a notification to the admin with action buttons
    user_name = update.effective_user.full_name
    admin_keyboard = [
        [
            InlineKeyboardButton("Ban User", callback_data=f"ban_user_{user_id}"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(admin_keyboard)

    admin_message_text = (
        f"An anonymous user has started a chat session.\n"
        f"Name: {user_name}\n"
        f"Chat ID: {user_id}"
    )
    
    # Store the user's ID to map to the admin chat
    context.bot_data['chat_session'] = user_id
    
    # Send the admin message and store its ID for reply context
    admin_message = await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=admin_message_text,
        reply_markup=reply_markup
    )
    # Store the admin message ID to enable replies
    context.user_data['admin_message_id'] = admin_message.message_id

    logger.info(f"Chat support started for user {user_id}")
    return CHAT_SUPPORT

async def handle_chat_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Forwards messages from the user to the admin.
    """
    user_id = update.effective_user.id
    if user_id == context.bot_data.get('chat_session'):
        try:
            admin_message_id = context.user_data.get('admin_message_id')
            await context.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=f"User ({user_id}): {update.message.text}",
                reply_to_message_id=admin_message_id
            )
            logger.info(f"User {user_id} sent message: '{update.message.text}'")
        except Exception as e:
            logger.error(f"Error forwarding message to admin: {e}")
            await update.effective_message.reply_text("There was an error sending your message. Please try again later.")

    return CHAT_SUPPORT

async def end_chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Ends the chat support conversation for both user and admin.
    """
    user_id = update.effective_user.id
    
    if user_id == ADMIN_CHAT_ID:
        # Admin ends the chat
        if context.bot_data.get('chat_session'):
            user_to_end = context.bot_data.pop('chat_session')
            context.user_data.pop('admin_message_id', None)
            
            await context.bot.send_message(
                chat_id=user_to_end,
                text="The chat session has been ended by the admin."
            )
            await update.effective_message.reply_text("You have ended the chat session.")
            logger.info(f"Admin ended chat with user {user_to_end}")
    
    elif context.bot_data.get('chat_session') == user_id:
        # User ends the chat
        await update.effective_message.reply_text(
            "The chat session has been ended. You can use /start to begin a new session."
        )
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"The user ({user_id}) has ended the chat session."
        )
        context.bot_data.pop('chat_session', None)
        context.user_data.pop('admin_message_id', None)
        logger.info(f"User {user_id} ended the chat.")

    return ConversationHandler.END

async def handle_admin_actions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles admin actions from inline buttons (like Ban).
    """
    query = update.callback_query
    await query.answer()

    if query.data.startswith("ban_user_"):
        user_id_to_ban = int(query.data.split("_")[-1])
        banned_users = load_banned_users()
        if user_id_to_ban not in banned_users:
            banned_users.append(user_id_to_ban)
            save_banned_users(banned_users)
            await query.edit_message_text(f"User {user_id_to_ban} has been banned.")
            logger.info(f"Admin {ADMIN_CHAT_ID} banned user {user_id_to_ban}.")
        else:
            await query.edit_message_text(f"User {user_id_to_ban} is already banned.")
            logger.info(f"Admin tried to ban an already banned user {user_id_to_ban}.")

        # End the chat session for the banned user
        if context.bot_data.get('chat_session') == user_id_to_ban:
            context.bot_data.pop('chat_session', None)
            await context.bot.send_message(
                chat_id=user_id_to_ban,
                text="You have been banned from using chat support. The session has been ended."
            )

async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles replies from the admin back to the anonymous user.
    """
    if update.effective_chat.id == ADMIN_CHAT_ID and update.message.reply_to_message:
        # The replied-to message is the user's forwarded message
        try:
            # We need to find the user's ID from the replied-to message
            original_text = update.message.reply_to_message.text
            user_id_str = original_text.split("User (")[-1].split("):")[0]
            user_id = int(user_id_str)
            
            await context.bot.send_message(
                chat_id=user_id,
                text=f"Admin: {update.message.text}"
            )
            logger.info(f"Admin replied to user {user_id}: '{update.message.text}'")
        except (ValueError, IndexError):
            # This handles cases where the message format is unexpected
            await update.effective_message.reply_text("Could not determine the user's chat ID from the message.")

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

        # Conversation handler for the chat support
        conv_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(start_chat_support, pattern="^start_chat_support$")],
            states={
                CHAT_SUPPORT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_chat_message)],
            },
            fallbacks=[CommandHandler("endchat", end_chat_command)],
        )

        # Add handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("endchat", end_chat_command))
        application.add_handler(CallbackQueryHandler(button_callback))
        application.add_handler(conv_handler)
        
        # Admin action handlers
        application.add_handler(MessageHandler(
            filters.REPLY & filters.User(ADMIN_CHAT_ID), handle_admin_reply
        ))
        application.add_handler(CallbackQueryHandler(
            handle_admin_actions, pattern="^ban_user_")
        )

        # Add error handler
        application.add_error_handler(error_handler)

        logger.info("Bot is starting...")
        print("🚀 Bot is starting...")
        print("💡 Remember to set your actual BOT_TOKEN and SHOP_URL!")
        print(f"💡 Your admin chat ID is set to: {ADMIN_CHAT_ID}.")
        print("🔄 Bot is running... Press Ctrl+C to stop.")

        application.run_polling(drop_pending_updates=True)

    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        print(f"❌ Failed to start bot: {e}")

if __name__ == '__main__':
    main()
