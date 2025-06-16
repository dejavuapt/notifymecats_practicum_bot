from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from pokeroom._pokeroom import Pokeroom
from pokeroom._pokeroomobject import Token, Team
from core.db import get_user_by_telegram_id

pokeroom: Pokeroom = Pokeroom()

async def get_teams(update: Update, cotnext: ContextTypes.DEFAULT_TYPE) -> None:
    teams: tuple[Team, ...] = await pokeroom.get_teams(
        access_token=get_user_by_telegram_id(update.effective_user.id).access_token
    )
    teamss = [team.name for team in teams]

    await update.message.reply_text(
        f"Is your teams: {teamss}",
        parse_mode="Markdown",
        # reply_markup=reply_keyboard
    ) 
    

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
                access_token=get_user_by_telegram_id(update.effective_user.id).access_token, 
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