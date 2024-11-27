import aiosqlite
from core.config import settings


async def create_db():
    async with aiosqlite.connect(settings.DATABASE_PATH) as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS participants (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            telegram_id INTEGER UNIQUE,
                            name TEXT)""")

        await db.execute("""CREATE TABLE IF NOT EXISTS groups (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            group_id INTEGER UNIQUE)""")

        await db.execute("""CREATE TABLE IF NOT EXISTS group_members (
                            group_id INTEGER,
                            telegram_id INTEGER,
                            FOREIGN KEY(group_id) REFERENCES groups(id),
                            FOREIGN KEY(telegram_id) REFERENCES participants(telegram_id))""")

        await db.execute("""CREATE TABLE IF NOT EXISTS duties (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            group_id INTEGER,
                            date TEXT,
                            main_id INTEGER,
                            reserve_id INTEGER,
                            FOREIGN KEY(group_id) REFERENCES groups(id),
                            FOREIGN KEY(main_id) REFERENCES participants(telegram_id),
                            FOREIGN KEY(reserve_id) REFERENCES participants(telegram_id))""")

        await db.commit()


async def add_participant(username: str, user_id: int):
    async with aiosqlite.connect(settings.DATABASE_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO participants (telegram_id, name) VALUES (?, ?)",
            (user_id, username),
        )
        await db.commit()


async def add_group(group_id: int):
    async with aiosqlite.connect(settings.DATABASE_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO groups (group_id) VALUES (?)",
            (group_id,),
        )
        await db.commit()


async def add_member_to_group(group_id: int, user_id: int):
    async with aiosqlite.connect(settings.DATABASE_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO group_members (group_id, telegram_id) VALUES (?, ?)",
            (group_id, user_id),
        )
        await db.commit()


async def get_participants_in_group(group_id: int) -> list:
    async with aiosqlite.connect(settings.DATABASE_PATH) as db:
        async with db.execute(
            "SELECT p.telegram_id, p.name FROM participants p "
            "JOIN group_members gm ON p.telegram_id = gm.telegram_id "
            "WHERE gm.group_id = ?",
            (group_id,),
        ) as cursor:
            participants = await cursor.fetchall()
            return [{"telegram_id": row[0], "name": row[1]} for row in participants]


async def get_duty_for_day(group_id: int, day: int) -> dict:
    async with aiosqlite.connect(settings.DATABASE_PATH) as db:
        cursor = await db.execute(
            "SELECT main_id, reserve_id FROM duties WHERE group_id = ? AND date = ?",
            (group_id, day),
        )
        duty = await cursor.fetchone()
    return {
        "main": duty[0] if duty else "Не определен",
        "reserve": duty[1] if duty else "Не определен",
    }


async def assign_duty(group_id: int, date: str, main_id: int, reserve_id: int):
    async with aiosqlite.connect(settings.DATABASE_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO duties (group_id, date, main_id, reserve_id) VALUES (?, ?, ?, ?)",
            (group_id, date, main_id, reserve_id),
        )
        await db.commit()


async def clear_group(group_id: int):
    async with aiosqlite.connect(settings.DATABASE_PATH) as db:
        await db.execute("DELETE FROM group_members WHERE group_id = ?", (group_id,))
        await db.execute("DELETE FROM duties WHERE group_id = ?", (group_id,))
        await db.commit()
