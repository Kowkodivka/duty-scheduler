import asyncio
from asyncio import Event

from duties import create_monthly_schedule
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message


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


async def get_holidays(message: Message, bot: AsyncTeleBot) -> list[int]:
    info_message = (
        "📅 Укажите праздничные дни в формате: `1, 4, 5, 9-12` или откажитесь, написав `нет`.\n"
        "Дни можно перечислять через запятую или диапазоны через дефис."
    )

    await bot.reply_to(message, info_message, parse_mode="Markdown")

    holidays = []
    response_event = Event()

    def is_author_message(target: Message):
        return (
            message.from_user.id == target.from_user.id and not response_event.is_set()
        )

    @bot.message_handler(func=is_author_message)
    async def process_holidays(target: Message):
        nonlocal holidays

        if "нет" in target.text.lower():
            await bot.reply_to(target, "✅ Праздничных дней нет.")
        else:
            input_text = target.text.replace(" ", "").strip(",")
            holidays = []

            for part in input_text.split(","):
                if "-" in part:
                    start, end = map(int, part.split("-"))
                    holidays.extend(range(start, end + 1))
                else:
                    holidays.append(int(part))

            holidays = sorted(set(holidays))

            await bot.reply_to(
                target, f"✅ Праздничные дни: {', '.join(map(str, holidays))}"
            )

        response_event.set()

    try:
        await asyncio.wait_for(response_event.wait(), timeout=60)
    except TimeoutError:
        await bot.send_message(
            message.chat.id, "⏳ Время вышло. Ответ на сообщение не был получен."
        )
        return []

    return holidays


async def start(message: Message, bot: AsyncTeleBot):
    usernames = await get_usernames(message, bot)
    if not usernames:
        return

    holidays = await get_holidays(message, bot)
    duties_schedule, formatted_schedule = create_monthly_schedule(usernames, holidays=holidays)

    await bot.reply_to(message, "```\n" + formatted_schedule + "\n```", parse_mode="Markdown")
