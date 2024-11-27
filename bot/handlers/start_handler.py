import asyncio
import os
from asyncio import Event
from datetime import datetime, timedelta

from duties import create_monthly_schedule
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from utils import save_holidays, save_schedule, save_usernames


async def get_usernames(message: Message, bot: AsyncTeleBot) -> list[str]:
    info_message = (
        "📝 Telegram не позволяет получить список участников группы автоматически. "
        "Пожалуйста, введите людей через пробел или упоминания (@username), которые будут дежурить:"
    )

    await bot.reply_to(message, info_message)

    usernames = []
    response_event = Event()

    def is_author_message(target: Message):
        return (
            message.from_user.id == target.from_user.id and not response_event.is_set()
        )

    @bot.message_handler(func=is_author_message)
    async def process_usernames(target: Message):
        nonlocal usernames

        if target.entities:
            usernames = [
                target.text[entity.offset + 1 : entity.offset + entity.length]
                for entity in target.entities
                if entity.type == "mention"
            ]
        else:
            usernames = target.text.split()

        usernames = [name.strip() for name in usernames if name.strip()]

        if usernames:
            await bot.reply_to(
                target,
                f"✅ Список сформирован: {', '.join(usernames)}",
            )
        else:
            await bot.reply_to(target, "❌ Список не был сформирован.")

        response_event.set()

    try:
        await asyncio.wait_for(response_event.wait(), timeout=60)
    except TimeoutError:
        await bot.send_message(
            message.chat.id, "⏳ Время вышло. Ответ на сообщение не был получен."
        )
        return []

    return usernames


async def get_holiday_dates(message: Message, bot: AsyncTeleBot) -> list[str]:
    info_message = (
        "📅 Укажите праздничные даты в формате: `2023-11-28, 2023-12-01` или диапазоны: `2023-12-01 - 2023-12-03`.\n"
        "Если праздничных дней нет, напишите `нет`.\n"
        "Даты указывайте в формате `YYYY-MM-DD`, разделяя запятыми или используя диапазоны через дефис."
    )

    await bot.reply_to(message, info_message, parse_mode="Markdown")

    holiday_dates = []
    response_event = Event()

    def is_author_message(target: Message):
        return (
            message.from_user.id == target.from_user.id and not response_event.is_set()
        )

    @bot.message_handler(func=is_author_message)
    async def process_holiday_dates(target: Message):
        nonlocal holiday_dates

        if "нет" in target.text.lower():
            await bot.reply_to(target, "✅ Праздничных дат нет.")
        else:
            input_text = target.text.replace(" ", "").strip(",")
            holiday_dates = []

            try:
                for part in input_text.split(","):
                    if "-" in part:
                        start_str, end_str = map(str.strip, part.split("-"))
                        start_date = datetime.strptime(start_str, "%Y-%m-%d")
                        end_date = datetime.strptime(end_str, "%Y-%m-%d")
                        current_date = start_date
                        while current_date <= end_date:
                            holiday_dates.append(current_date.strftime("%Y-%m-%d"))
                            current_date += timedelta(days=1)
                    else:
                        single_date = datetime.strptime(part.strip(), "%Y-%m-%d")
                        holiday_dates.append(single_date.strftime("%Y-%m-%d"))

                holiday_dates = sorted(set(holiday_dates))

                await bot.reply_to(
                    target, f"✅ Праздничные даты: {', '.join(holiday_dates)}"
                )
            except ValueError:
                await bot.reply_to(
                    target,
                    "❌ Ошибка: Проверьте формат ввода. Даты должны быть в формате `YYYY-MM-DD`.",
                )
                return

        response_event.set()

    try:
        await asyncio.wait_for(response_event.wait(), timeout=60)
    except TimeoutError:
        await bot.send_message(
            message.chat.id, "⏳ Время вышло. Ответ на сообщение не был получен."
        )
        return []

    return holiday_dates


async def start(message: Message, bot: AsyncTeleBot):
    if int(os.getenv("CHAT_ID")) != message.chat.id:
        return

    usernames = await get_usernames(message, bot)

    if not usernames:
        return

    holidays = await get_holiday_dates(message, bot)

    duties_schedule, formatted_schedule = create_monthly_schedule(usernames, holidays)

    save_schedule(duties_schedule)
    save_usernames(usernames)
    save_holidays(holidays)

    await bot.reply_to(
        message, "```\n" + formatted_schedule + "\n```", parse_mode="Markdown"
    )
