from datetime import datetime


async def send_daily_reminder(bot, chat_id, schedule):
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
                f"Пожалуйста, не забудьте о своих обязанностях. Спасибо! 😊"
            )

            await bot.send_message(chat_id, reminder_message, parse_mode="Markdown")
