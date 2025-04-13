import os
import asyncio
import threading
from fastapi import FastAPI
import uvicorn
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.error import BadRequest

TOKEN = os.getenv('BOT_TOKEN')
if TOKEN is None:
    raise ValueError("Токен не найден в переменных окружения!")

# Бот-команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Приветик🌸🌸🌸, сможешь зайти зарегистрироваться в боте, после я увижу твой ник и сразу же кину подарочек, вот [@vodka_bot](https://t.me/vodka_ref_bot?start=6605634314) ⭐⭐⭐",
        parse_mode='Markdown'
    )
    await update.message.reply_text(
        "Нужно подписаться на тгк и просто зайти на сайт, после в боте нажать «Я все выполнил», после у вас в чате с ботом должно быть сообщение 'Главное меню'."
    )
    await update.message.reply_text("Только после этого ты получишь подарок.")
    keyboard = [[InlineKeyboardButton("Я подписался", callback_data='subscribed')]]
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Подпишись на канал и нажми кнопку ниже.", reply_markup=markup)

async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = await context.bot.get_chat_member("@FEH1KC", update.callback_query.from_user.id)
        if user.status in ['member', 'administrator', 'creator']:
            await update.callback_query.answer("Вы подписаны!")
            await update.callback_query.edit_message_text("Спасибо! Ждите подарок.")
        else:
            raise Exception()
    except:
        await update.callback_query.answer("Подпишись на канал.")
        await update.callback_query.edit_message_text("Ты не подписан. Подпишись и нажми снова.")


def run_telegram_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_subscription, pattern='^subscribed$'))
    app.run_polling()

threading.Thread(target=run_telegram_bot).start()


fastapi_app = FastAPI()

@fastapi_app.get("/")
def read_root():
    return {"status": "Bot is running"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(fastapi_app, host="0.0.0.0", port=port)
