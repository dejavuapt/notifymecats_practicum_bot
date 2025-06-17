from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from pokeroom._pokeroom import Pokeroom
from pokeroom._teamobject import Team
from core.db import get_user_by_telegram_id

pokeroom: Pokeroom = Pokeroom()

async def get_teams(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    teams: tuple[Team, ...] = await pokeroom.get_teams(
        access_token=get_user_by_telegram_id(update.effective_user.id).access_token
    )
    if not teams:
        await update.message.reply_text("Sorry. You haven't teams. You can create with /create_team command.")
        return

    keyboard = [
        [InlineKeyboardButton(f"{team.name} {team.user_role}", callback_data=f"team_{team.id}")] for team in teams
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Choose a team from the list below:",
        parse_mode="Markdown",
        reply_markup=reply_markup
    ) 

async def handle_team_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    # keyboard = [ [InlineKeyboardButton("<<", callback_data="")] ]
    # reply_markup = InlineKeyboardMarkup(keyboard)
    team_info: Team = await pokeroom.get_team_info(
        access_token=get_user_by_telegram_id(update.effective_user.id).access_token,
        id=query.data.replace("team_", "")
    )
    
    await query.edit_message_text(
        f"Here it is: *{team_info.name}*\n"
        f"Description: *{team_info.description}*\n\n"
        f"Your are *{team_info.user_role.lower()}* in team",
        # "\nWhat do you want to do with the team?",
        parse_mode="Markdown",
        reply_markup=None
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