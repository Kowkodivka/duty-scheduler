import asyncio
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
from utils import load_chat_id, load_schedule, load_usernames

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = AsyncTeleBot(BOT_TOKEN, colorful_logs=True, parse_mode="HTML")

scheduler = AsyncIOScheduler()


async def send_daily():
    await send_daily_reminder(bot, load_chat_id(), load_schedule(), load_usernames())


async def send_monthly():
    await generate_monthly_schedule(bot)


scheduler.add_job(send_daily, CronTrigger(hour=8, minute=0, second=0, day_of_week="mon-sun"))
scheduler.add_job(send_monthly, CronTrigger(hour=16, minute=0, second=0, day=31))


if __name__ == "__main__":
    handlers = [start, info, ping]

    for handler in handlers:
        bot.register_message_handler(
            handler, commands=[handler.__name__], pass_bot=True
        )

    asyncio.run(bot.polling(non_stop=True))
