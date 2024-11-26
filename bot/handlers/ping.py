import time

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

ping_router = Router()


@ping_router.message(Command("ping"))
async def ping_handler(message: Message) -> None:
    start = time.monotonic()
    sent_message = await message.answer("🏓 Проверка задержки...")
    end = time.monotonic()
    await sent_message.edit_text(f"🏓 Задержка: {round((end - start) * 1000, 2)} мс")
