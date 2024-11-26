from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

start_router = Router()


@start_router.message(Command("start"))
async def start_handler(message: Message) -> None:
    start_message = (
        "Бот для планирования графика дежурств.\n"
        "Создан @thelucin, весь мой код лежит на GitHub, вот тут:\n"
        "📂 https://github.com/Kowkodivka/duty-scheduler\n\n"
        "Всегда рад обратной связи. 🛠️"
    )

    await message.reply(start_message)
