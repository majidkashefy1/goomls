from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from config import TOKEN
from scraper import run_scraper
from parser import extract_leads, export_csv
from storage import user_state, STATE_WAIT_QUERY, STATE_IDLE


# ---------------- UI HELPERS ----------------

def format_leads(leads):
    if not leads:
        return "❌ No results found."

    msg = "📊 Leads Found:\n\n"

    for l in leads:
        msg += (
            f"🏪 {l.get('name')}\n"
            f"📞 {l.get('phone')}\n"
            f"📍 {l.get('address')}\n"
            "----------------------\n"
        )

    return msg


# ---------------- START MENU ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔍 Search Places", callback_data="search")],
        [InlineKeyboardButton("📂 Last Result", callback_data="last")],
        [InlineKeyboardButton("❓ Help", callback_data="help")]
    ]

    await update.message.reply_text(
        "👋 Welcome to Lead Finder Bot",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ---------------- BUTTON HANDLER ----------------

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data == "search":
        user_state[user_id] = STATE_WAIT_QUERY

        await query.message.reply_text(
            "✍️ Send your search query:\n"
            "Example: coffee shop in Isfahan"
        )

    elif query.data == "help":
        await query.message.reply_text(
            "Just click 🔍 Search Places and send your query."
        )

    elif query.data == "last":
        await query.message.reply_text("🚧 Last result feature not enabled yet.")


# ---------------- MESSAGE HANDLER ----------------

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    state = user_state.get(user_id, STATE_IDLE)

    if state != STATE_WAIT_QUERY:
        await update.message.reply_text("👉 Click 🔍 Search Places first.")
        return

    user_state[user_id] = STATE_IDLE

    await update.message.reply_text("🔎 Searching Google Maps...")

    try:
        csv_path = run_scraper(text)

        leads = extract_leads(csv_path)

        await update.message.reply_text(format_leads(leads))

        file_path = export_csv(leads)

        await update.message.reply_document(document=open(file_path, "rb"))

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


# ---------------- MAIN ----------------

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()