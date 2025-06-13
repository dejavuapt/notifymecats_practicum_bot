from telegram import Update, Chat, ReplyKeyboardMarkup
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
    
async def register_in_pokeroom(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Какой у тебя никнейм?")
    return USERNAME

async def recieve_username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['username'] = update.message.text
    await update.message.reply_text("Напиши свою почту")
    return EMAIL

async def recieve_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['email'] = update.message.text
    await update.message.reply_text("Ну а теперь пароль")
    return PASSWORD

async def recieve_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    password = update.message.text
    username = context.user_data['username']
    email = context.user_data['email']
    
    try:
        tokens: Token = await pokeroom.registration_in_service(
            user_data={
                "username": username,
                "email": email,
                "password": password,
                "telegram_id": update.effective_user.id
            }
        )
        await update.message.reply_text(f"ТЕСТ: {tokens.access}")   
    except Exception as exp:
        print(str(exp))
        await update.message.reply_text("Упс, что-то пошло не так")
    
    return ConversationHandler.END