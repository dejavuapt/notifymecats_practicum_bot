from telegram import Bot, Update, Chat, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters

from core import settings
from bot.methods import (
    send_cat_image, 
    wake_up_samurai, 
    register_in_pokeroom,
    recieve_email,
    recieve_username,
    recieve_password
)
from bot.methods import USERNAME, EMAIL, PASSWORD

# like or not like cat or funny sad
logger = settings.logging.getLogger(__name__)

def main() -> None:
    bot: Bot = Bot(token = settings.BOT_TOKEN)    
    app: Application = Application.builder().bot(bot).build() # паттерн строителя
    
    # Очередь имеет значение. от частного к общему!
    # app.add_handler(CommandHandler(command='newcat', callback=send_cat_image))
    app.add_handler(CommandHandler(command='start', callback=wake_up_samurai))
    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler(command='register', callback=register_in_pokeroom)],
        states={
            USERNAME: [MessageHandler(filters=filters.TEXT, callback=recieve_username)],
            EMAIL: [MessageHandler(filters=filters.TEXT, callback=recieve_email)],
            PASSWORD: [MessageHandler(filters=filters.TEXT, callback=recieve_password)],
        },
        fallbacks=[]
    ))
    
    # poll_interval также блокирует на 20 секунд дело 0.0 итак базово стоит
    app.run_polling(allowed_updates=Update.ALL_TYPES, poll_interval=2.0)

# Запуск программы грубо говоря выполнятся только тогда когда данный файл является исполняемым, т.е. pythone3 main.py, __name__ указывает на то исполняемый это файл т.е. main или же это импортированный модуль
if __name__ == "__main__":
    main()