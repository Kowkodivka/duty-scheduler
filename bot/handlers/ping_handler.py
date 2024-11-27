import time

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message


async def ping(message: Message, bot: AsyncTeleBot):
    start = time.monotonic()
    sent_message = await bot.reply_to(message, "🏓 Проверка задержки...")
    end = time.monotonic()
    await bot.edit_message_text(
        f"🏓 Задержка: {round((end - start) * 1000, 2)} мс",
        sent_message.chat.id,
        sent_message.message_id,
    )
