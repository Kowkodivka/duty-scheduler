from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message


async def info(message: Message, bot: AsyncTeleBot):
    info_message = (
        "Бот для планирования графика дежурств.\n"
        "Создан @thelucin, весь мой код лежит на GitHub, вот тут:\n"
        "📂 https://github.com/Kowkodivka/duty-scheduler\n\n"
        "Всегда рад обратной связи. 🛠️"
    )

    await bot.reply_to(message, info_message)
