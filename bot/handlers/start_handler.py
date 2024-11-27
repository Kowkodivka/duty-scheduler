import asyncio

from duties import create_monthly_schedule, format_schedule
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message


async def start(message: Message, bot: AsyncTeleBot):
    info_message = (
        "📝 Из-за ограничений Telegram получить список участников группы невозможно. "
        "Пожалуйста, вручную через пробел введите людей, которые будут дежурить:"
    )
    sent_message = await bot.reply_to(message, info_message)

    def is_author_reply(msg):
        return (
            msg.reply_to_message
            and msg.reply_to_message.message_id == sent_message.message_id
            and msg.from_user.id == message.from_user.id
        )

    students = []
    active = True

    @bot.message_handler(func=is_author_reply)
    async def process_students(target):
        nonlocal students, active

        students = [
            {"id": entity.user.id, "name": entity.user.username}
            for entity in target.entities
            if entity.type == "mention" and entity.user
        ]

        active = False

        if students:
            await bot.reply_to(
                target,
                f"✅ Список сформирован: {', '.join([s['name'] for s in students])}",
            )
        else:
            await bot.reply_to(target, "❌ Список не был сформирован.")

    await asyncio.sleep(60)

    if active:
        await bot.send_message(
            message.chat.id, "⏳ Время вышло. Ответ на сообщение не был получен."
        )
        return

    duties_schedule = create_monthly_schedule(students)
    formatted_schedule = format_schedule(duties_schedule, students)

    await bot.reply_to(message, formatted_schedule)
