import os
import logging
import aiofiles
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Берём токен из Environment Variable
TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(level=logging.INFO)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Для бронирования места на Хэллоуин напиши, пожалуйста, немного о себе: \n1. Фамилия Имя @никнейм. \n2. Возвраст. \n3. Являешься ли студентом/выпусником мехмата? \n4. Если ты не с мехмата, расскажи, откуда ты узнал о мероприятии?")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    user = msg.from_user
    timestamp = msg.date.isoformat()
    username = f"@{user.username}" if user.username else "<no-username>"
    line = f"{timestamp} | user_id={user.id} | {username} | {user.full_name} | {msg.text}\n"
    
    async with aiofiles.open("messages.txt", mode="a", encoding="utf-8") as f:
        await f.write(line)
    
    await update.message.reply_text("Спасибо! Место забронировано! Чуть позже Ксения свяжется с тобой.")

def main():
    # Новый способ создания приложения для python-telegram-bot 22+
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    app.run_polling()

if __name__ == "__main__":
    main()
