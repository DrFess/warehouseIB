import sqlite3
import os
from settings import PATH_TO_DB


def connection_to_DB(func):
    """Декоратор - подключение к базе данных"""
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(
            os.path.abspath(PATH_TO_DB),
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        result = func(cursor, *args, **kwargs)

        conn.commit()
        cursor.close()
        conn.close()

        return result
    return wrapper


def connection_to_DB_without_datetype(func):
    """Декоратор - подключение к базе данных без настроек типов"""
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(
            os.path.abspath(PATH_TO_DB)
        )
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        result = func(cursor, *args, **kwargs)

        conn.commit()
        cursor.close()
        conn.close()

        return result
    return wrapper


@connection_to_DB
def create_tables(cursor, table_name: str):
    """Создание таблиц базы данных"""
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS {table_name}(
                                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                            telegram_id INTEGER,
                                            surname TEXT,
                                            name TEXT,
                                            patronymic TEXT,
                                            group_id INTEGER,
                                            FOREIGN KEY (group_id) REFERENCES student_group(id) ON DELETE CASCADE
        )""",
    )
    return f'Таблица {table_name} создана'

