import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.error import BadRequest

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = "@FEH1KC"

if not TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Приветик🌸🌸🌸, сможешь зайти зарегистрироваться в боте, после я увижу твой ник и сразу же кину подарочек, вот [@vodka_bot](https://t.me/vodka_ref_bot?start=6605634314) ⭐⭐⭐",
        parse_mode='Markdown'
    )
    await update.message.reply_text("Нужно подписаться на тгк и просто зайти на сайт, после в боте нажать «Я все выполнил», после у вас в чате с ботом должно быть сообщение 'Главное меню'.")
    await update.message.reply_text("Только после этого ты получишь подарок.")

    keyboard = [[InlineKeyboardButton("Я подписался", callback_data='subscribed')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Чтобы продолжить, пожалуйста, подпишитесь на наш канал и нажмите кнопку «Я подписался».",
        reply_markup=reply_markup
    )

async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.callback_query.from_user.id
    try:
        member = await context.bot.get_chat_member(CHANNEL, user_id)
        if member.status in ["member", "administrator", "creator"]:
            await update.callback_query.answer("Вы подписаны на канал!")
            await update.callback_query.edit_message_text("Спасибо за подписку! Теперь ты в очереди на получение подарка.")
        else:
            await update.callback_query.answer("Вы не подписаны на канал.")
            await update.callback_query.edit_message_text("Ты не подписан на канал. Подпишись и нажми «Я подписался» снова.")
    except BadRequest:
        await update.callback_query.answer("Ошибка: не удалось проверить подписку.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(check_subscription, pattern="^subscribed$"))

app.run_polling()
