import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Մենյուի տվյալները
with open("menu.json", "r", encoding="utf-8") as f:
    menu = json.load(f)

def find_dish(query):
    for item in menu:
        if query.lower() in item["name_hy"].lower() or query.lower() in item["name_en"].lower():
            return item
    return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Բարև ☺️ Ես Sorriso բոթն եմ, օգնեմ իմանալ՝ ուտեստը պարունակում է ալերգեններ թե ոչ։ Գրիր ուտեստի անունը։")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    dish = find_dish(text)

    if dish:
        allergens = ", ".join(dish["allergens"])
        if text.isascii():
            response = f"{dish['name_en']} contains: {allergens}."
        else:
            response = f"{dish['name_hy']} պարունակում է՝ {allergens}"
    else:
        response = "Նման ուտեստ չգտա 😔"

    await update.message.reply_text(response)

async def main():
    token = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
