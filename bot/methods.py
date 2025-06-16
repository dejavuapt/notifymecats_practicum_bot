from telegram import Update, Chat, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
import hashlib
from telegram.ext import ContextTypes, ConversationHandler
from core import catapi
from pokeroom._pokeroom import Pokeroom
from pokeroom._pokeroomobject import Token, Team

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
    
async def create_team(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """ Starts the conversation and asks for team name. """
    await update.message.reply_text(
        "Alright, a new team. How are we going to call it? Please choose a name for your team."
    ) 
    return 0

async def receive_team_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["team_name"] = update.message.text
    await update.message.reply_text(
        f"Great name! You choose a {context.user_data.get("team_name")} team name.\n\n"
        "Wanna write description? If yes just typing it:"
    )
    return 1



async def receive_team_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    
    context.user_data["team_description"] = update.message.text
    team_info = (
        f"📝 *Your new team*\n"
        f"• Name: {context.user_data.get("team_name")}\n"
        f"• Description: {context.user_data.get("team_description")}"
    )

    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data="yes"),
            InlineKeyboardButton("No", callback_data="no"),
        ]
    ]
    reply_keyboard = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"{team_info}\n\n"
        "Confirm information?",
        parse_mode="Markdown",
        reply_markup=reply_keyboard
    )
    return 2


async def confirmed_information_team(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    
    query = update.callback_query
    await query.answer()
    
    if query.data == "yes":
        try:
            registered_team: Team = await pokeroom.create_team(
                "",
                name=context.user_data.get("team_name"),
                description=context.user_data.get("team_description") or None
            )
            pokeroom._LOGGER.debug(f"Team success created: {registered_team.name}, {registered_team.description}")
            await query.edit_message_text(
                text="✅ Team created! use /get_teams to get more information!\n",
                reply_markup=None
            )
        except Exception as exp:
            pokeroom._LOGGER.error(str(exp))
            raise
    else:
        await query.edit_message_text(
            "❌ Team create cancelled.\n",
            reply_markup=None
        )
            
    context.user_data.clear()   
    return ConversationHandler.END