from telegram import Update 
import hashlib
from telegram.ext import ContextTypes
from pokeroom._pokeroom import Pokeroom
from pokeroom._pokeroomobject import Token, Team
from core.db import create_user
from typing import Any

pokeroom: Pokeroom = Pokeroom()


async def register_in_pokeroom(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    hashed_password = hashlib\
        .sha256(string=f"{update.effective_user.id}{update.effective_user.name}".encode())\
        .hexdigest()[:20]
    
    chat_user = update.effective_user
    try:
        user_data: dict[str, Any] = {
            "first_name": chat_user.first_name,
            "last_name": chat_user.last_name,
            "username": chat_user.name,
            "telegram_id": str(chat_user.id)
        }
        print(user_data)
        user_data.update({"password": hashed_password,})
        tokens: Token = await pokeroom.registration_in_service(
            user_data=user_data
        )
        pokeroom._LOGGER.debug(f"Success register \n {tokens.access} \n {tokens.refresh}")
        user_data.pop("password")
        user_data.update({"access_token": tokens.access, "refresh_token": tokens.refresh})
        create_user(
            **user_data
        )
        await update.message.reply_text("\
                                        🚀 Yo! Success registration!\
                                        ")
    except Exception as exp:
        pokeroom._LOGGER.debug(f"Something was wrong: {str(exp)}")
        await update.message.reply_text("\
                                        🤖 Sorry. Something was wrong. Try again later...\
                                        ")