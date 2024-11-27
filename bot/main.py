import asyncio
import os
from collections.abc import Callable
from datetime import datetime, timedelta

from dotenv import load_dotenv
from handlers.info_handler import info
from handlers.ping_handler import ping
from handlers.start_handler import start
from reminders.daily import send_daily_reminder
from telebot.async_telebot import AsyncTeleBot

load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN")

bot = AsyncTeleBot(BOT_TOKEN, colorful_logs=True, parse_mode="HTML")


async def schedule_reminders(bot, chat_id, duties_schedule, participants):
    now = datetime.now()

    next_reminder = datetime.combine(now.date(), datetime.min.time()) + timedelta(hours=8)

    if now > next_reminder:
        next_reminder += timedelta(days=1)

    while True:
        wait_time = (next_reminder - datetime.now()).total_seconds()
        await asyncio.sleep(wait_time)
        await send_daily_reminder(bot, chat_id, duties_schedule, participants)
        next_reminder += timedelta(days=1)


if __name__ == "__main__":
    handlers: [Callable] = [start, info, ping]

    for handler in handlers:
        bot.register_message_handler(
            handler, commands=[handler.__name__], pass_bot=True
        )

    asyncio.run(bot.polling(non_stop=True))
