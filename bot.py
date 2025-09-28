from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import aiofiles
import os
import logging

TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(level=logging.INFO)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Для бронирования места на Хэллоуин напиши, пожалуйста, немного о себе: \n1. Фамилия Имя @никнейм. \n2. Возвраст. \n3. Являешься ли студентом/выпусником мехмата? \n4. Если ты не с мехмата, расскажи, откуда ты узнал о мероприятии?")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    user = msg.from_user
    line = f"{user.id} | {msg.text}\n"
    async with aiofiles.open("messages.txt", "a", encoding="utf-8") as f:
        await f.write(line)
    await update.message.reply_text("Спасибо! Место забронировано! Чуть позже Ксения свяжется с тобой.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()
