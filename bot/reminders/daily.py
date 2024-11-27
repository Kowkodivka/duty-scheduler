import os
from datetime import datetime

from utils import load_schedule


async def send_daily_reminder(bot):
    try:
        schedule = load_schedule()

        current_day = datetime.now().day

        if current_day in schedule:
            main = schedule[current_day].get("main")
            reserve = schedule[current_day].get("reserve", "Нет")

            if main:
                reminder_message = (
                    f"📢 *Напоминание о дежурстве на сегодня!*\n\n"
                    f"📅 Сегодня *{datetime.now().strftime('%d.%m.%Y')}*\n\n"
                    f"👤 *Дежурный*: {main}\n"
                    f"🔄 *Резерв*: {reserve}\n\n"
                    f"Пожалуйста, не забудьте о своих обязанностях. Спасибо!"
                )

                await bot.send_message(int(os.getenv("CHAT_ID")), reminder_message, parse_mode="Markdown")

    except FileNotFoundError:
        await bot.send_message(
            int(os.getenv("CHAT_ID")),
            "Пользователи не инициализированы. Пожалуйста, используйте команду /start.",
            parse_mode="Markdown",
        )
