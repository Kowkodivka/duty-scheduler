from datetime import datetime


async def send_daily_reminder(bot, chat_id, duties_schedule, participants):
    today = datetime.now().day

    if today in duties_schedule:
        id_to_name = {
            participant["id"]: participant["name"] for participant in participants
        }

        duty = duties_schedule[today]

        main = id_to_name.get(duty["main"], "Нет")
        reserve = id_to_name.get(duty["reserve"], "Нет")

        mentions = " ".join(f"@{name}" for name in [main, reserve] if name != "Нет")

        await bot.send_message(
            chat_id,
            f"🔔 Напоминание: Сегодня дежурят:\n⭐ Основной: {main}\n🛠️ Резервный: {reserve}\n{mentions}",
        )
