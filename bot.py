from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from scraper import run_scraper
from parser import extract_leads, export_csv

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"


def format_text(leads):
    if not leads:
        return "No valid leads found."

    msg = "📊 Leads Found:\n\n"

    for l in leads:
        msg += (
            f"🏪 {l.get('name','')}\n"
            f"📞 {l.get('phone','')}\n"
            f"📍 {l.get('address','')}\n"
            f"---------------------\n"
        )

    return msg


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send a query like:\ncoffee shop in Chahar Bagh Isfahan"
    )


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text

    await update.message.reply_text("🔍 Searching Google Maps...")

    try:
        csv_path = run_scraper(query)

        leads = extract_leads(csv_path)

        if not leads:
            await update.message.reply_text("No results found.")
            return

        # 1) text response
        text = format_text(leads)
        await update.message.reply_text(text)

        # 2) export clean CSV
        clean_path = export_csv(leads)

        # 3) send file to telegram
        await update.message.reply_document(document=open(clean_path, "rb"))

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()