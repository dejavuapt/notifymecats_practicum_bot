from telegram import Bot, Update, Chat, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters, CallbackQueryHandler
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
import os, sys

from core import settings
from bot.methods import (
    wake_up_samurai, 
    register_in_pokeroom,
    create_team,
    receive_team_name,
    receive_team_description,
    confirmed_information_team,
)

# like or not like cat or funny sad
logger = settings.logging.getLogger(__name__)

def main() -> None:
    bot: Bot = Bot(token = settings.BOT_TOKEN)    
    app: Application = Application.builder().bot(bot).build() # паттерн строителя
    
    # Очередь имеет значение. от частного к общему!
    # app.add_handler(CommandHandler(command='newcat', callback=send_cat_image))
    app.add_handler(CommandHandler(command='start', callback=wake_up_samurai))
    app.add_handler(CommandHandler(command='register', callback=register_in_pokeroom)) 
    
    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler(command="create_team", callback=create_team)],
        states={
            0: [MessageHandler(filters=filters.TEXT, callback=receive_team_name)],
            1: [MessageHandler(filters=filters.TEXT, callback=receive_team_description)],
            2: [CallbackQueryHandler(callback=confirmed_information_team)]
        },
        fallbacks=[]
    ))
    app.run_polling(allowed_updates=Update.ALL_TYPES, poll_interval=2.0)

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self._callback = callback
        self._restart = False

    def on_any_event(self, event: FileSystemEvent):
        if event.is_directory or event.src_path.endswith(".py"):
            if not self._restart:
                print(f"Changed in {event.src_path}. Restart")
                self._restart = True
                self._callback()

def watch_files():
    def restart_bot():
        print("Bot restarting...")
        os.execv(sys.executable, ['python'] + sys.argv)

    event_handler = FileChangeHandler(restart_bot)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)  # Отслеживать текущую папку
    observer.start()

    try:
        main()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Запуск программы грубо говоря выполнятся только тогда когда данный файл является исполняемым, т.е. pythone3 main.py, __name__ указывает на то исполняемый это файл т.е. main или же это импортированный модуль
if __name__ == "__main__":
    watch_files()