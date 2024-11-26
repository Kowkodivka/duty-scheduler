from datetime import date

from aiosqlite import Connection


async def create_tables(database: Connection) -> None:
    await database.execute("""
    CREATE TABLE IF NOT EXISTS groups (
        group_id INTEGER PRIMARY KEY NOT NULL
    )
    """)

    await database.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY NOT NULL,
        group_id INTEGER NOT NULL
    )
    """)

    await database.execute("""
    CREATE TABLE IF NOT EXISTS duties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        group_id INTEGER NOT NULL,
        week_number INTEGER NOT NULL,
        day_of_week INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (group_id) REFERENCES groups(group_id)
    )
    """)

    await database.execute("""
    CREATE TABLE IF NOT EXISTS exclusions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id INTEGER NOT NULL,
        excluded_date DATE NOT NULL,
        is_temporary BOOLEAN NOT NULL,
        FOREIGN KEY (group_id) REFERENCES groups(group_id)
    )
    """)

    await database.commit()


async def add_user(database: Connection, user_id: int, group_id: int) -> None:
    await database.execute(
        "INSERT OR REPLACE INTO users (user_id, group_id) VALUES (?, ?)",
        (user_id, group_id)
    )
    await database.commit()


async def get_users(database: Connection, group_id: int) -> [int]:
    cursor = await database.execute(
        "SELECT user_id FROM users WHERE group_id = ?", (group_id,)
    )
    users = await cursor.fetchall()
    return [user[0] for user in users]


async def clear_users(database: Connection, group_id: int) -> None:
    await database.execute(
        "DELETE FROM users WHERE group_id = ?",
        (group_id)
    )
    await database.commit()


async def add_exclusion(database: Connection, group_id: int, excluded_date: date, is_temporary: bool) -> None:
    await database.execute("""
    INSERT INTO exclusions (group_id, excluded_date, is_temporary)
    VALUES (?, ?, ?)
    """, (group_id, excluded_date, is_temporary))
    await database.commit()


async def get_exclusions(database: Connection, group_id: int) -> [date]:
    cursor = await database.execute(
        "SELECT excluded_date FROM exclusions WHERE group_id = ?",
        (group_id)
    )
    exclusions = await cursor.fetchall()
    return {excluded_date[0] for excluded_date in exclusions}


async def clear_exclusions(database: Connection, group_id: int) -> None:
    await database.execute(
        "DELETE FROM exclusions WHERE group_id = ?",
        (group_id)
    )
    await database.commit()


async def shuffle_duties(database: Connection, group_id: int, per_day: int, weekdays: [str]) -> None:
    pass
