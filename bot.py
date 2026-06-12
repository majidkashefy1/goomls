import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from scraper import run_scraper
from parser import extract_leads

TOKEN = "8709408508:AAG9pAhrkerRJIWhYbiiSn2_wRMf4Mdzy34"


def format_results(leads):
    if not leads:
        return "No results found."

    msg = ""
    for l in leads[:10]:
        msg += f"""
🏪 {l['name']}
📞 {l['phone']}
📍 {l['address']}
----------------------
"""
    return msg


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a place (e.g. coffee shop in Isfahan)")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text

    await update.message.reply_text("🔍 Searching Google Maps...")

    try:
        csv_path = run_scraper(query)
        leads = extract_leads(csv_path)

        response = format_results(leads)

        await update.message.reply_text(response)

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()