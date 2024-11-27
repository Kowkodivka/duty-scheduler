from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message
from core.config import settings
from core.database import add_participant

register_router = Router()


@register_router.message(Command("add_all"))
async def add_all_participants(message: Message):
    bot = Bot(token=settings.BOT_TOKEN)
    chat_id = message.chat.id
    members = await bot.get_chat_members(chat_id)

    for member in members:
        if member.user.is_bot:
            continue

        await add_participant(member.user.username, member.user.id)

    await message.answer("Все участники добавлены в систему.")
