import json
import os

import aiofiles

INFO_FILE = "./info.json"


async def save_schedule(schedule: dict) -> None:
    data = await _load_info_file()
    data["schedule"] = schedule
    await _save_info_file(data)


async def load_schedule() -> dict:
    data = await _load_info_file()
    if "schedule" not in data:
        raise FileNotFoundError()
    return data["schedule"]


async def save_usernames(usernames: list) -> None:
    data = await _load_info_file()
    data["usernames"] = usernames
    await _save_info_file(data)


async def load_usernames() -> list:
    data = await _load_info_file()
    if "usernames" not in data:
        raise FileNotFoundError()
    return data["usernames"]


async def save_holidays(holidays: list) -> None:
    data = await _load_info_file()
    data["holidays"] = holidays
    await _save_info_file(data)


async def load_holidays() -> list:
    data = await _load_info_file()
    if "holidays" not in data:
        raise FileNotFoundError()
    return data["holidays"]


async def _load_info_file() -> dict:
    if not os.path.exists(INFO_FILE):
        return {}
    async with aiofiles.open(INFO_FILE) as file:
        content = await file.read()
        return json.loads(content)


async def _save_info_file(data: dict) -> None:
    async with aiofiles.open(INFO_FILE, "w") as file:
        await file.write(json.dumps(data, indent=4))
