import asyncio
import logging
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
from handlers.info_handler import info
from handlers.ping_handler import ping
from handlers.start_handler import start
from reminders.daily import send_daily_reminder
from reminders.monthly import generate_monthly_schedule
from telebot.async_telebot import AsyncTeleBot

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TIME_ZONE = os.getenv("TIME_ZONE")
CHAT_ID = os.getenv("CHAT_ID")


bot = AsyncTeleBot(BOT_TOKEN, parse_mode="HTML")
scheduler = AsyncIOScheduler(timezone=TIME_ZONE)

logging.basicConfig(level=logging.INFO)

logging.getLogger("apscheduler").setLevel(logging.DEBUG)
logging.getLogger("telebot").setLevel(logging.DEBUG)


async def send_daily():
    await send_daily_reminder(bot)


async def send_monthly():
    await generate_monthly_schedule(bot)


async def main():
    handlers = [start, info, ping]

    for handler in handlers:
        bot.register_message_handler(handler, commands=[handler.__name__], pass_bot=True)

    scheduler.start()

    scheduler.add_job(
        send_daily,
        CronTrigger(hour=8, minute=0, second=0, day_of_week="*"),
        id="daily_reminder",
    )

    scheduler.add_job(
        send_monthly,
        CronTrigger(hour=16, minute=0, second=0, day="last"),
        id="monthly_schedule",
    )

    await bot.polling(non_stop=True)


if __name__ == "__main__":
    asyncio.run(main())
