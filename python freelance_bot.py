import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# Replace with your bot token from @BotFather
BOT_TOKEN = "7619805071:AAHnzNTqjPJQdwXpvJx2eY0hFSqcL7WFaOc"

# Enable logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Sample freelancer and client data storage
freelancers = {}
clients = {}

async def start(update: Update, context):
    """Welcome message with options."""
    keyboard = [
        [InlineKeyboardButton("📌 Register as Freelancer", callback_data="register_freelancer")],
        [InlineKeyboardButton("💼 Hire a Freelancer", callback_data="hire_freelancer")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to Swift Talent Forge! 🚀\nChoose an option:", reply_markup=reply_markup)

async def button_handler(update: Update, context):
    """Handles button clicks."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "register_freelancer":
        await query.message.reply_text("📌 Please send your skills and portfolio link.")
        return

    if query.data == "hire_freelancer":
        await query.message.reply_text("💼 Send the job details (Title, Budget, and Requirements).")
        return

async def register_freelancer(update: Update, context):
    """Stores freelancer details."""
    user_id = update.message.from_user.id
    freelancers[user_id] = update.message.text
    await update.message.reply_text("✅ You are now registered as a freelancer! Clients can see your profile.")

async def post_job(update: Update, context):
    """Stores client job details."""
    user_id = update.message.from_user.id
    clients[user_id] = update.message.text
    await update.message.reply_text("📌 Your job has been posted! Freelancers will be notified.")

def main():
    """Start the bot."""
    app = Application.builder().token(BOT_TOKEN).build()

    # Command Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, register_freelancer))

    # Run the bot
    app.run_polling()

if __name__ == "__main__":
    main()
