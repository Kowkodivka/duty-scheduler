import os

from duties import create_monthly_schedule
from telebot.async_telebot import AsyncTeleBot
from utils import load_holidays, load_usernames, save_schedule


async def generate_monthly_schedule(bot: AsyncTeleBot):
    try:
        usernames = await load_usernames()
        holidays = await load_holidays()

        duties_schedule, formatted_schedule = create_monthly_schedule(usernames, holidays)

        await save_schedule(duties_schedule)

        await bot.send_message(
            int(os.getenv("CHAT_ID")),
            "```\n" + formatted_schedule + "\n```",
            parse_mode="Markdown",
        )

    except FileNotFoundError:
        await bot.send_message(
            int(os.getenv("CHAT_ID")),
            "Ошибка: Пользователи не инициализированы. Пожалуйста, используйте команду /start.",
            parse_mode="Markdown",
        )
