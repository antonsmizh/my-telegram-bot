import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.error import BadRequest
from fastapi import FastAPI
import uvicorn
import asyncio

# Получаем токен из переменной окружения
TOKEN = os.getenv('BOT_TOKEN')

if TOKEN is None:
    raise ValueError("Токен не найден в переменных окружения! Убедитесь, что вы добавили BOT_TOKEN на Render.")

# Создаем FastAPI приложение
app = FastAPI()

# Этот эндпоинт будет нужен для Render, чтобы показывать, что сервис работает
@app.get("/")
def read_root():
    return {"message": "Bot is running!"}

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

    keyboard = [
        [InlineKeyboardButton("Я подписался", callback_data='subscribed')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Чтобы продолжить, пожалуйста, подпишитесь на наш канал и нажмите кнопку «Я подписался».",
        reply_markup=reply_markup
    )

async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.callback_query.from_user.id
    try:
        user_info = await context.bot.get_chat_member(chat_id, "@FEH1KC")
        if user_info.status in ['member', 'administrator', 'creator']:
            await update.callback_query.answer("Вы подписаны на канал!")
            await update.callback_query.edit_message_text("Спасибо за подписку! Теперь ты в очереди на получение подарка.")
        else:
            await update.callback_query.answer("Вы не подписаны на канал. Пожалуйста, подпишитесь, чтобы продолжить.")
            await update.callback_query.edit_message_text("Ты не подписан на канал. Подпишись и нажми «Я подписался» снова.")
    except BadRequest as e:
        await update.callback_query.answer(f"Ошибка: {e.message}")

# Получаем порт из переменной окружения, если он не установлен, то используем порт 10000
port = os.getenv("PORT", 10000)

# Инициализация бота
bot = ApplicationBuilder().token(TOKEN).build()

# Добавляем обработчики
bot.add_handler(CommandHandler("start", start))
bot.add_handler(CallbackQueryHandler(check_subscription, pattern='^subscribed$'))

# Запускаем бота в фоновом режиме
async def start_bot():
    await bot.start_polling()

# Для Render запускаем FastAPI приложение и бота параллельно
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    
    # Запускаем FastAPI сервер
    loop.create_task(uvicorn.run(app, host="0.0.0.0", port=port))
    
    # Запускаем Telegram бота
    loop.create_task(start_bot())
    
    loop.run_forever()


