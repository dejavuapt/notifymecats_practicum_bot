from telegram import Update, Chat, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from core import catapi

async def send_cat_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat: Chat = update.effective_chat
    await context.bot.send_photo(chat_id=chat.id, photo=catapi.get_url_cat_image())

async def wake_up_samurai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat: Chat = update.effective_chat
    name: str = update.message.chat.first_name
    button: ReplyKeyboardMarkup = ReplyKeyboardMarkup([['/newcat']], resize_keyboard=True)
    await context.bot.send_message(
        chat_id=chat.id, 
        text=f'Хей, {name}! У меня есть для тебя котик, посмотри!',
        reply_markup=button
    )