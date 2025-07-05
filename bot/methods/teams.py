from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from pokeroom._pokeroom import Pokeroom
from pokeroom._teamobject import Team
from pokeroom._tokenobject import Token
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
        [InlineKeyboardButton(f"{"👑" if team.user_role == "Owner" else "👤"} {team.name}", callback_data=f"team_{team.id}")] for team in teams
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query = update.callback_query
    message_data = {"text": f"Choose a team from the list below:",
                    "parse_mode": "Markdown",
                    "reply_markup": reply_markup}
    if query:
        await query.edit_message_text(**message_data)
    else:
        await update.message.reply_text(**message_data) 

async def handle_team_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    data = query.data
    team_id = data.replace("team_", "")
    team = await pokeroom.get_team(team_id=team_id,
                                   access_token=get_user_by_telegram_id(update.effective_user.id).access_token)
    
    keyboard = [ [InlineKeyboardButton("get members", callback_data=f"members_{team_id}"), 
                  InlineKeyboardButton("poker", callback_data=f"poker{team_id}")],
                 [InlineKeyboardButton("gen invite code", callback_data=f"invite_{team_id}"),
                  InlineKeyboardButton("<<", callback_data="back_to_teams")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"👥 Here it is: *{team.name}*\n"
        f"You are a {team.user_role}"
        "\nWhat do you want to do?",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
    
async def get_team_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    data = query.data
    team_id = data.replace("members_", "")
    members_of_team = await pokeroom.get_members_of_team(team_id=team_id,
                                                         access_token=get_user_by_telegram_id(update.effective_user.id).access_token) 
    pokeroom._LOGGER.warning(members_of_team)
    owner_into_text: str = "👑 <b>Owner:</b> \n"
    members_into_text: str = "👥 <b>Members:</b> \n"
    if len(members_of_team) == 1:
        members_into_text += "There is no one\n"

    for member in members_of_team:
        if member.role == "Owner":
            owner_into_text += member.username
        else:
            members_into_text += f"&#8226; {member.username}\n"
    
    await query.edit_message_text(
        f"{owner_into_text}\n\n{members_into_text}",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<<", callback_data=f"team_{team_id}")]])
    )
    

async def create_team(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """ Starts the conversation and asks for team name. """
    await update.message.reply_text(
        "Alright, a new team. How are you going to call it? Please choose a name for your team."
    ) 
    return 0

async def receive_team_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["team_name"] = update.message.text
    await update.message.reply_text(
        f"Great name! You choose a \"{context.user_data.get("team_name")}\" team name.\n\n"
        "Please write a description for you team."
    )
    return 1



async def receive_team_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    
    context.user_data["team_description"] = update.message.text
    team_info = (
        f"📝 *Your new team*\n"
        f"• Name: \"{context.user_data.get("team_name")}\"\n"
        f"• Description: \"{context.user_data.get("team_description")}\""
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