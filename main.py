#!/usr/bin/env python3
"""
Online Shop Telegram Bot
Compatible with Python 3.13 and python-telegram-bot library
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration - replace with your actual values
BOT_TOKEN = "7054945394:AAGbjMWSwcH_MGQCoorLVBhBxF6tJd9KcQg"
SHOP_CHANNEL = "https://t.me/your_channel_name"
INSTAGRAM_URL = "https://www.instagram.com/hacksagex/"
SUPPORT_USERNAME = "@your_support_username"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command with shop main menu"""
    try:
        user = update.effective_user
        welcome_message = (
            f"🛍️ Welcome to our Online Shop, {user.first_name}!\n\n"
            "🎯 Your one-stop destination for quality products\n"
            "Choose from the options below:"
        )
        
        keyboard = [
            [InlineKeyboardButton("🛒 Browse Products", callback_data="browse_products")],
            [InlineKeyboardButton("📦 My Orders", callback_data="my_orders")],
            [InlineKeyboardButton("🎁 Special Offers", callback_data="offers")],
            [InlineKeyboardButton("📞 Customer Support", callback_data="support")],
            [InlineKeyboardButton("⭐ Reviews", callback_data="reviews")],
            [InlineKeyboardButton("ℹ️ Shop Info", callback_data="shop_info")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_message, reply_markup=reply_markup)
        logger.info(f"Start command sent to user {user.id}")
        
    except Exception as e:
        logger.error(f"Error in start_command: {e}")
        await update.message.reply_text("Sorry, something went wrong. Please try again later.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show available commands for shop"""
    try:
        help_text = (
            "🛍️ **Shop Commands:**\n\n"
            "/start - Shop main menu\n"
            "/help - Show this help\n"
            "/products - Browse all products\n"
            "/orders - Check your orders\n"
            "/offers - Current deals & offers\n"
            "/contact - Contact support\n"
            "/track - Track your order\n\n"
            "💡 Use the menu buttons for easy navigation!"
        )
        
        keyboard = [[InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(help_text, reply_markup=reply_markup, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Error in help_command: {e}")

async def products_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show products directly"""
    await show_products_menu_message(update.message)

async def orders_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show orders directly"""
    await show_orders_menu_message(update.message)

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show contact info directly"""
    contact_text = (
        "📞 **Contact Our Support Team**\n\n"
        "💬 Telegram Support: @your_support_username\n"
        "📧 Email: support@yourshop.com\n"
        "⏰ Working Hours: 9 AM - 9 PM (Mon-Sat)\n"
        "📱 WhatsApp: +91-XXXXXXXXXX\n\n"
        "We're here to help with:\n"
        "• Product inquiries\n"
        "• Order assistance\n"
        "• Returns & refunds\n"
        "• Technical support"
    )
    
    keyboard = [
        [InlineKeyboardButton("💬 Contact Support", url=f"https://t.me/{SUPPORT_USERNAME.replace('@', '')}")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(contact_text, reply_markup=reply_markup, parse_mode='Markdown')

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button clicks from inline keyboards"""
    try:
        query = update.callback_query
        await query.answer()
        
        if query.data == "main_menu":
            await show_main_menu(query)
        elif query.data == "browse_products":
            await show_products_menu(query)
        elif query.data == "my_orders":
            await show_orders_menu(query)
        elif query.data == "offers":
            await show_offers_menu(query)
        elif query.data == "support":
            await show_support_menu(query)
        elif query.data == "reviews":
            await show_reviews_menu(query)
        elif query.data == "shop_info":
            await show_shop_info(query)
        elif query.data == "categories":
            await show_categories(query)
        elif query.data == "search_products":
            await search_products_info(query)
        elif query.data == "track_order":
            await track_order_info(query)
        elif query.data == "order_history":
            await show_order_history(query)
        elif query.data == "current_offers":
            await show_current_offers(query)
        elif query.data == "new_arrivals":
            await show_new_arrivals(query)
        elif query.data == "best_sellers":
            await show_best_sellers(query)
        elif query.data == "return_policy":
            await show_return_policy(query)
        elif query.data == "shipping_info":
            await show_shipping_info(query)
        elif query.data == "payment_methods":
            await show_payment_methods(query)
        
    except Exception as e:
        logger.error(f"Error in button_callback: {e}")
        try:
            await query.answer("Something went wrong. Please try again.")
        except:
            pass

async def show_main_menu(query):
    """Show the main shop menu"""
    welcome_message = (
        "🛍️ **Online Shop - Main Menu**\n\n"
        "Choose what you'd like to do:"
    )
    
    keyboard = [
        [InlineKeyboardButton("🛒 Browse Products", callback_data="browse_products")],
        [InlineKeyboardButton("📦 My Orders", callback_data="my_orders")],
        [InlineKeyboardButton("🎁 Special Offers", callback_data="offers")],
        [InlineKeyboardButton("📞 Customer Support", callback_data="support")],
        [InlineKeyboardButton("⭐ Reviews", callback_data="reviews")],
        [InlineKeyboardButton("ℹ️ Shop Info", callback_data="shop_info")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(welcome_message, reply_markup=reply_markup, parse_mode='Markdown')

async def show_products_menu(query):
    """Show products browsing options"""
    products_message = (
        "🛒 **Browse Our Products**\n\n"
        "Find exactly what you're looking for:"
    )
    
    keyboard = [
        [InlineKeyboardButton("📱 View All Products", url=SHOP_CHANNEL)],
        [InlineKeyboardButton("📂 Categories", callback_data="categories")],
        [InlineKeyboardButton("🔥 Best Sellers", callback_data="best_sellers")],
        [InlineKeyboardButton("🆕 New Arrivals", callback_data="new_arrivals")],
        [InlineKeyboardButton("🔍 Search Products", callback_data="search_products")],
        [InlineKeyboardButton("🏠 Back to Main Menu", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(products_message, reply_markup=reply_markup, parse_mode='Markdown')

async def show_orders_menu(query):
    """Show order management options"""
    orders_message = (
        "📦 **Order Management**\n\n"
        "Track and manage your orders:"
    )
    
    keyboard = [
        [InlineKeyboardButton("🔍 Track Order", callback_data="track_order")],
        [InlineKeyboardButton("📋 Order History", callback_data="order_history")],
        [InlineKeyboardButton("🔄 Return/Exchange", callback_data="return_policy")],
        [InlineKeyboardButton("📞 Order Support", url=f"https://t.me/{SUPPORT_USERNAME.replace('@', '')}")],
        [InlineKeyboardButton("🏠 Back to Main Menu", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(orders_message, reply_markup=reply_markup, parse_mode='Markdown')

async def show_offers_menu(query):
    """Show current offers and deals"""
    offers_message = (
        "🎁 **Special Offers & Deals**\n\n"
        "Don't miss out on amazing savings!"
    )
    
    keyboard = [
        [InlineKeyboardButton("🔥 Current Offers", callback_data="current_offers")],
        [InlineKeyboardButton("⚡ Flash Sales", url=SHOP_CHANNEL)],
        [InlineKeyboardButton("💰 Discount Codes", callback_data="discount_codes")],
        [InlineKeyboardButton("🎯 Bundle Deals", callback_data="bundle_deals")],
        [InlineKeyboardButton("🏠 Back to Main Menu", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(offers_message, reply_markup=reply_markup, parse_mode='Markdown')

async def show_support_menu(query):
    """Show customer support options"""
    support_message = (
        "📞 **Customer Support**\n\n"
        "We're here to help you 24/7:"
    )
    
    keyboard = [
        [InlineKeyboardButton("💬 Live Chat", url=f"https://t.me/{SUPPORT_USERNAME.replace('@', '')}")],
        [InlineKeyboardButton("❓ FAQ", callback_data="faq")],
        [InlineKeyboardButton("📧 Email Support", callback_data="email_support")],
        [InlineKeyboardButton("🚚 Shipping Info", callback_data="shipping_info")],
        [InlineKeyboardButton("💳 Payment Help", callback_data="payment_methods")],
        [InlineKeyboardButton("🏠 Back to Main Menu", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(support_message, reply_markup=reply_markup, parse_mode='Markdown')

async def show_reviews_menu(query):
    """Show reviews and testimonials"""
    reviews_message = (
        "⭐ **Customer Reviews**\n\n"
        "See what our customers say about us:"
    )
    
    keyboard = [
        [InlineKeyboardButton("📱 View on Instagram", url=INSTAGRAM_URL)],
        [InlineKeyboardButton("⭐ Leave a Review", callback_data="leave_review")],
        [InlineKeyboardButton("📊 Our Ratings", callback_data="our_ratings")],
        [InlineKeyboardButton("📸 Customer Photos", url=INSTAGRAM_URL)],
        [InlineKeyboardButton("🏠 Back to Main Menu", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(reviews_message, reply_markup=reply_markup, parse_mode='Markdown')

async def show_shop_info(query):
    """Show shop information"""
    shop_info_message = (
        "ℹ️ **About Our Shop**\n\n"
        "🏪 **Shop Name:** Your Online Store\n"
        "📅 **Established:** 2020\n"
        "🌍 **Location:** India\n"
        "📦 **Products:** 500+ Items\n"
        "⭐ **Rating:** 4.8/5\n"
        "🚚 **Delivery:** Pan India\n\n"
        "✅ **Why Choose Us:**\n"
        "• Genuine products only\n"
        "• Fast & secure delivery\n"
        "• 24/7 customer support\n"
        "• Easy returns & refunds\n"
        "• Best prices guaranteed"
    )
    
    keyboard = [
        [InlineKeyboardButton("🚚 Shipping Policy", callback_data="shipping_info")],
        [InlineKeyboardButton("🔄 Return Policy", callback_data="return_policy")],
        [InlineKeyboardButton("💳 Payment Methods", callback_data="payment_methods")],
        [InlineKeyboardButton("🏠 Back to Main Menu", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(shop_info_message, reply_markup=reply_markup, parse_mode='Markdown')

async def show_categories(query):
    """Show product categories"""
    categories_message = (
        "📂 **Product Categories**\n\n"
        "Browse by category:"
    )
    
    keyboard = [
        [InlineKeyboardButton("👕 Fashion & Clothing", url=SHOP_CHANNEL)],
        [InlineKeyboardButton("📱 Electronics", url=SHOP_CHANNEL)],
        [InlineKeyboardButton("🏠 Home & Living", url=SHOP_CHANNEL)],
        [InlineKeyboardButton("💄 Beauty & Care", url=SHOP_CHANNEL)],
        [InlineKeyboardButton("⚽ Sports & Fitness", url=SHOP_CHANNEL)],
        [InlineKeyboardButton("🏠 Back to Products", callback_data="browse_products")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(categories_message, reply_markup=reply_markup, parse_mode='Markdown')

async def show_current_offers(query):
    """Show current offers"""
    offers_message = (
        "🔥 **Current Offers**\n\n"
        "💥 **MEGA SALE - 50% OFF**\n"
        "Valid till: This Weekend\n\n"
        "🎯 **Buy 2 Get 1 FREE**\n"
        "On selected items\n\n"
        "💰 **Flat ₹500 OFF**\n"
        "On orders above ₹2000\n"
        "Code: SAVE500\n\n"
        "🚚 **FREE SHIPPING**\n"
        "On all orders above ₹999"
    )
    
    keyboard = [
        [InlineKeyboardButton("🛍️ Shop Now", url=SHOP_CHANNEL)],
        [InlineKeyboardButton("🏠 Back to Offers", callback_data="offers")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(offers_message, reply_markup=reply_markup, parse_mode='Markdown')

async def track_order_info(query):
    """Show order tracking info"""
    track_message = (
        "🔍 **Track Your Order**\n\n"
        "To track your order, please send us:\n"
        "📋 Your Order ID\n"
        "📱 Registered Phone Number\n\n"
        "**Format:** \n"
        "Order ID: #12345\n"
        "Phone: +91XXXXXXXXXX\n\n"
        "Our support team will help you track your order instantly!"
    )
    
    keyboard = [
        [InlineKeyboardButton("💬 Send Order Details", url=f"https://t.me/{SUPPORT_USERNAME.replace('@', '')}")],
        [InlineKeyboardButton("🏠 Back to Orders", callback_data="my_orders")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(track_message, reply_markup=reply_markup, parse_mode='Markdown')

async def show_shipping_info(query):
    """Show shipping information"""
    shipping_message = (
        "🚚 **Shipping Information**\n\n"
        "📦 **Delivery Time:**\n"
        "• Metro Cities: 2-3 days\n"
        "• Other Cities: 4-7 days\n"
        "• Remote Areas: 7-10 days\n\n"
        "💰 **Shipping Charges:**\n"
        "• FREE on orders ₹999+\n"
        "• ₹99 for orders below ₹999\n\n"
        "📋 **What we need:**\n"
        "• Complete address\n"
        "• PIN code\n"
        "• Contact number\n\n"
        "✅ We ship pan India!"
    )
    
    keyboard = [[InlineKeyboardButton("🏠 Back", callback_data="shop_info")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(shipping_message, reply_markup=reply_markup, parse_mode='Markdown')

async def show_payment_methods(query):
    """Show payment methods"""
    payment_message = (
        "💳 **Payment Methods**\n\n"
        "We accept all major payment methods:\n\n"
        "💳 **Cards:**\n"
        "• Debit Cards\n"
        "• Credit Cards\n"
        "• International Cards\n\n"
        "📱 **Digital Payments:**\n"
        "• Google Pay\n"
        "• PhonePe\n"
        "• Paytm\n"
        "• UPI\n\n"
        "🏦 **Banking:**\n"
        "• Net Banking\n"
        "• Bank Transfer\n\n"
        "💰 **Cash on Delivery**\n"
        "Available in select areas"
    )
    
    keyboard = [[InlineKeyboardButton("🏠 Back", callback_data="shop_info")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(payment_message, reply_markup=reply_markup, parse_mode='Markdown')

async def show_products_menu_message(message):
    """Show products menu as a new message"""
    products_message = (
        "🛒 **Browse Our Products**\n\n"
        "Find exactly what you're looking for:"
    )
    
    keyboard = [
        [InlineKeyboardButton("📱 View All Products", url=SHOP_CHANNEL)],
        [InlineKeyboardButton("📂 Categories", callback_data="categories")],
        [InlineKeyboardButton("🔥 Best Sellers", callback_data="best_sellers")],
        [InlineKeyboardButton("🆕 New Arrivals", callback_data="new_arrivals")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await message.reply_text(products_message, reply_markup=reply_markup, parse_mode='Markdown')

async def show_orders_menu_message(message):
    """Show orders menu as a new message"""
    orders_message = (
        "📦 **Order Management**\n\n"
        "Track and manage your orders:"
    )
    
    keyboard = [
        [InlineKeyboardButton("🔍 Track Order", callback_data="track_order")],
        [InlineKeyboardButton("📋 Order History", callback_data="order_history")],
        [InlineKeyboardButton("🔄 Return/Exchange", callback_data="return_policy")],
        [InlineKeyboardButton("📞 Order Support", url=f"https://t.me/{SUPPORT_USERNAME.replace('@', '')}")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await message.reply_text(orders_message, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages from users"""
    try:
        text = update.message.text.lower()
        
        # Order tracking
        if "order" in text and "#" in text:
            await update.message.reply_text(
                "🔍 **Order Inquiry Received!**\n\n"
                "Our support team will help you track your order.\n"
                "Please contact our support for immediate assistance."
            )
        
        # Product inquiry
        elif any(word in text for word in ['price', 'cost', 'buy', 'purchase', 'product']):
            keyboard = [
                [InlineKeyboardButton("🛒 Browse Products", url=SHOP_CHANNEL)],
                [InlineKeyboardButton("💬 Contact Support", url=f"https://t.me/{SUPPORT_USERNAME.replace('@', '')}")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                "🛍️ **Looking for products?**\n\n"
                "Check our product catalog or contact support for personalized assistance!",
                reply_markup=reply_markup
            )
        
        else:
            # Default response for unrecognized messages
            keyboard = [[InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                "👋 Hello! I'm your shopping assistant.\n"
                "Use /help to see available commands or click the menu below:",
                reply_markup=reply_markup
            )
    
    except Exception as e:
        logger.error(f"Error in handle_text_message: {e}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors that occur during bot operation"""
    logger.error(f"Update {update} caused error {context.error}")

def main() -> None:
    """Main function to set up and run the shop bot"""
    try:
        # Create the Application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("products", products_command))
        application.add_handler(CommandHandler("orders", orders_command))
        application.add_handler(CommandHandler("contact", contact_command))
        
        # Add callback query handler for inline buttons
        application.add_handler(CallbackQueryHandler(button_callback))
        
        # Add message handler for text messages
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
        
        # Add error handler
        application.add_error_handler(error_handler)
        
        # Log startup
        logger.info("Online Shop Bot is starting...")
        print("🛍️ Online Shop Bot is starting...")
        print(f"📱 Shop Channel: {SHOP_CHANNEL}")
        print(f"📷 Instagram: {INSTAGRAM_URL}")
        print(f"📞 Support: {SUPPORT_USERNAME}")
        print("💡 Make sure to replace URLs with actual values!")
        print("🔄 Bot is running... Press Ctrl+C to stop.")
        
        # Run the bot
        application.run_polling(drop_pending_updates=True)
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        print(f"❌ Failed to start bot: {e}")

if __name__ == '__main__':
    main()
