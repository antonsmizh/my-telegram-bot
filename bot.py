import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv


load_dotenv()


TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text(
        "Приветик🌸🌸🌸, сможешь зайти зарегистрироваться в боте, после я увижу твой ник и сразу же кину подарочек, вот [@vodka_bot](https://t.me/vodka_ref_bot?start=6605634314) ⭐⭐⭐",
        parse_mode='Markdown'
    )
    
   
    await update.message.reply_text(
        "Нужно подписаться на тгк и просто зайти на сайт, после в боте нажать «Я все выполнил», после у вас в чате с ботом должно быть сообщение 'Главное меню'."
    )
    
    
    await update.message.reply_text(
        "Только после этого ты получишь подарок."
    )


app = ApplicationBuilder().token(TOKEN).build()


app.add_handler(CommandHandler("start", start))


app.run_polling()
