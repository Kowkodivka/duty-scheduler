from datetime import datetime


def generate_duties(participants: [dict], month: int, year: int) -> dict:
    first_day = datetime(year, month, 1)

    next_month = (
        first_day.replace(month=month % 12 + 1, day=1)
        if month < 12
        else first_day.replace(year=year + 1, month=1, day=1)
    )

    days_in_month = (next_month - first_day).days
    holidays = set()

    schedule = {}
    n_participants = len(participants)
    main_idx, reserve_idx = 0, 1

    for day in range(1, days_in_month + 1):
        if day in holidays:
            schedule[day] = {"main": None, "reserve": None}
        else:
            main_id = participants[main_idx]["id"]
            reserve_id = participants[reserve_idx]["id"]
            schedule[day] = {"main": main_id, "reserve": reserve_id}
            main_idx = (main_idx + 1) % n_participants
            reserve_idx = (reserve_idx + 1) % n_participants

    return schedule


def format_schedule(duties_schedule: dict, participants: list) -> str:
    id_to_name = {
        participant["id"]: participant["name"] for participant in participants
    }

    formatted_days = []

    for day, duty in duties_schedule.items():
        main = id_to_name.get(duty["main"], "Нет")
        reserve = id_to_name.get(duty["reserve"], "Нет")
        formatted_days.append(f"{day:02d}: ⭐ Основной: {main}, 🛠️ Резервный: {reserve}")

    return "\n".join(formatted_days)


async def create_monthly_schedule(participants):
    current_month = datetime.now().month
    current_year = datetime.now().year

    duties_schedule = generate_duties(participants, current_month, current_year)

    return duties_schedule
