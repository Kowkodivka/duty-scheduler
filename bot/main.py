import asyncio
import os

from dotenv import load_dotenv
from handlers.info_handler import info
from handlers.ping_handler import ping
from handlers.start_handler import start
from telebot.async_telebot import AsyncTeleBot

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = AsyncTeleBot(BOT_TOKEN, colorful_logs=True, parse_mode="HTML")


if __name__ == "__main__":
    handlers = [start, info, ping]

    for handler in handlers:
        bot.register_message_handler(
            handler, commands=[handler.__name__], pass_bot=True
        )

    asyncio.run(bot.polling(non_stop=True))
