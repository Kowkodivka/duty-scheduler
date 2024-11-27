import asyncio
import logging
import sys
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.daily import DailyTrigger
from core.config import settings
from core.database import get_duty_for_day
from telethon import TelegramClient


async def send_daily_duties(client: TelegramClient, chat_id: int):
    now = datetime.now()
    duty_info = await get_duty_for_day(now.day)

    main_duty = duty_info.get("main")
    reserve_duty = duty_info.get("reserve")

    message = f"Сегодня, {now.strftime('%Y-%m-%d')}, дежурят:\n"
    message += f"Основной: {main_duty}\nРезервный: {reserve_duty}"

    await client.send_message(chat_id, message)


async def main() -> None:
    client = TelegramClient("bot", settings.API_ID, settings.API_HASH)

    await client.start(bot_token=settings.BOT_TOKEN)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        send_daily_duties,
        DailyTrigger(hour=8, minute=0, second=0, timezone="Asia/Novokuznetsk"),
        args=[client, settings.CHAT_ID],
    )

    scheduler.start()

    await client.run_until_disconnected()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
