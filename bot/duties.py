import calendar
from datetime import datetime, timedelta

from prettytable import PrettyTable


def generate_duties(
    usernames: list[str], month: int, year: int, holidays: list[int] = None
) -> dict:
    holidays = holidays or []

    first_day = datetime(year, month, 1)

    next_month = (
        first_day.replace(month=month % 12 + 1, day=1)
        if month < 12
        else first_day.replace(year=year + 1, month=1, day=1)
    )

    days_in_month = (next_month - first_day).days

    for day in range(1, days_in_month + 1):
        current_date = first_day + timedelta(days=day - 1)
        if current_date.weekday() in (5, 6):
            holidays.append(day)

    schedule = {}
    n_participants = len(usernames)
    main_idx, reserve_idx = 0, 1

    for day in range(1, days_in_month + 1):
        if day in holidays:
            schedule[day] = {"main": None, "reserve": None}
        else:
            main_id = usernames[main_idx]
            reserve_id = usernames[reserve_idx]
            schedule[day] = {"main": main_id, "reserve": reserve_id}
            main_idx = (main_idx + 1) % n_participants
            reserve_idx = (reserve_idx + 1) % n_participants

    return schedule


def format_schedule(duties_schedule: dict, month: int, year: int) -> str:
    month_names = [
        "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
        "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
    ]

    month_name = month_names[month - 1]
    header = f"📅 Расписание дежурств: {month_name} {year}\n\n"
    days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    day_of_week = calendar.monthrange(year, month)[0]

    table = PrettyTable()
    table.field_names = ["№", "День недели", "Основной", "Резервный"]

    for day in range(1, 32):
        if day not in duties_schedule:
            continue

        weekday = days_of_week[(day_of_week + (day - 1)) % 7]
        main = duties_schedule[day].get("main") or "Нет"
        reserve = duties_schedule[day].get("reserve") or "Нет"

        table.add_row([day, weekday, main, reserve])

    return header + str(table)


def create_monthly_schedule(usernames: list[str], holidays: list[str]) -> (str, str):
    current_month = datetime.now().month
    current_year = datetime.now().year

    duties_schedule = generate_duties(usernames, current_month, current_year, holidays)
    return duties_schedule, format_schedule(
        duties_schedule, current_month, current_year
    )
