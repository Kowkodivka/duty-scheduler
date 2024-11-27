import json

import aiosqlite

DB_PATH = "database.db"


async def create_tables():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY,
                participants TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS schedules (
                group_id INTEGER PRIMARY KEY,
                schedule TEXT,
                FOREIGN KEY(group_id) REFERENCES groups(id) ON DELETE CASCADE
            )
        """)
        await db.commit()


async def register_group(group_id: int, participants: list[dict[str, str]]):
    async with aiosqlite.connect(DB_PATH) as db:
        participants_json = json.dumps(participants)
        await db.execute(
            """
            INSERT INTO groups (id, participants)
            VALUES (?, ?)
            ON CONFLICT(id) DO UPDATE SET participants = excluded.participants
        """,
            (group_id, participants_json),
        )
        await db.commit()


async def remove_group(group_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM groups WHERE id = ?", (group_id,))
        await db.commit()


async def register_schedule(group_id: int, schedule: dict[str, dict[str, str]]):
    async with aiosqlite.connect(DB_PATH) as db:
        schedule_json = json.dumps(schedule)
        await db.execute(
            """
            INSERT INTO schedules (group_id, schedule)
            VALUES (?, ?)
            ON CONFLICT(group_id) DO UPDATE SET schedule = excluded.schedule
        """,
            (group_id, schedule_json),
        )
        await db.commit()


async def get_schedule(group_id: int) -> dict[str, dict[str, str]] | None:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT schedule FROM schedules WHERE group_id = ?", (group_id,)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return json.loads(row[0])
    return None
