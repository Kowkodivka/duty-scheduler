from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from core.database import get_duty_for_day

duties_router = Router()


@duties_router.message(Command("duties"))
async def duties_for_day(message: Message):
    args = message.get_args()
    if args:
        try:
            date = args.strip()
            duty = await get_duty_for_day(date)
            if duty:
                main_name = duty[0]
                reserve_name = duty[1]
                await message.answer(
                    f"В день {date} дежурят:\nОсновной: {main_name}\nРезервный: {reserve_name}"
                )
            else:
                await message.answer(f"На {date} нет дежурства.")
        except ValueError:
            await message.answer("Неверный формат даты. Используйте YYYY-MM-DD.")
    else:
        await message.answer("Укажите дату для получения информации о дежурстве.")
