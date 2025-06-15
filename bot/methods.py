from telegram import Update, Chat, ReplyKeyboardMarkup
import hashlib
from telegram.ext import ContextTypes, ConversationHandler
from core import catapi
from pokeroom._pokeroom import Pokeroom
from pokeroom._pokeroomobject import Token

pokeroom: Pokeroom = Pokeroom()

async def send_cat_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat: Chat = update.effective_chat
    await context.bot.send_photo(chat_id=chat.id, photo=catapi.get_url_cat_image())

async def wake_up_samurai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat: Chat = update.effective_chat
    name: str = update.message.chat.first_name
    button: ReplyKeyboardMarkup = ReplyKeyboardMarkup([['/register']], resize_keyboard=True)
    await context.bot.send_message(
        chat_id=chat.id, 
        text=f'Хей, {name}! Давай зарегистрируемся и сыграем в покер планирование!',
        reply_markup=button
    )
    
    
USERNAME, EMAIL, PASSWORD = range(3)
    
async def register_in_pokeroom(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    hashed_password = hashlib\
        .sha256(string=f"{update.effective_user.id}{update.effective_user.name}".encode())\
        .hexdigest()[:20]
    
    print(update.message.chat.id) 
    try:
        tokens: Token = await pokeroom.registration_in_service(
            user_data={
                "first_name": update.effective_chat.first_name,
                "second_name": update.effective_user.last_name,
                "username": update.effective_user.name,
                "password": hashed_password,
                "telegram_id": update.effective_user.id
            }
        )
        pokeroom._LOGGER.debug(f"Success register \n {tokens.access} \n {tokens.refresh}")
        await update.message.reply_text("\
                                        🚀 Yo! Success registration!\
                                        ")
    except Exception as exp:
        pokeroom._LOGGER.debug(f"Something was wrong: {str(exp)}")
        await update.message.reply_text("\
                                        🤖 Sorry. Something was wrong. Try again later...\
                                        ")
    