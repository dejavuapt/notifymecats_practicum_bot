import os
import dotenv
import logging

dotenv.load_dotenv()
BOT_TOKEN: str = os.environ["BOT_TOKEN"]

URL_CATS: str = 'https://api.thecatapi.com/v1/images/search'
# URL_CATS: str = ''
URL_DOGS: str = 'https://api.thedogapi.com/v1/images/search'

# format:
# asctime - время события, levelname - уровень важности, name - имя логгера, message - тескст сообщения
# %-форматирование, s - указывается тип строка. Для чисел - d.
# https://docs.python.org/3/library/logging.html#logrecord-attributes
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s(%(filename)s/%(funcName)s:%(lineno)d): %(message)s || Created at %(asctime)s by %(name)s", #\x1b[33;20m \x1b[0m
    # filename='main.log',
    # filemode='w',
)

logger = logging.getLogger("core")

DATABASE = {
    "ENGINE": os.getenv("DB_ENGINE", "sqlite"),
    "NAME": os.getenv("DB_NAME")
}

def build_database_url(settings: dict) -> str:
    engine:str = settings.get("ENGINE")
    if engine == "sqlite":
        return f"sqlite:///{settings.get('NAME')}"

    raise ValueError(f"Unsupported DB engine: {engine}")


DATABASE_URL = build_database_url(DATABASE)