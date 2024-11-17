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
def create_tables(cursor):
    """Создание таблиц базы данных"""
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS manufacturers (
                                                manufacturer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                manufacturer_title VARCHAR(255) NOT NULL,
                                                address VARCHAR(255)
        )""",
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS products (
                                                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                barcode INTEGER,
                                                product_name VARCHAR(255) NOT NULL,
                                                price_product INTEGER,
                                                weight_per_unit DECIMAL(10, 2),
                                                manufacturer_id INTEGER,
                                                FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(manufacturer_id)
        )""",
    )
    return 'База данных создана'


@connection_to_DB
def db_add_manufacturer(cursor, manufacturer_title: str, address: str) -> str:
    """Добавление производителя"""
    cursor.execute(
        """INSERT INTO manufacturers (manufacturer_title, address)
                                    VALUES (?, ?)""",
        (manufacturer_title, address)
    )
    return f'Производитель {manufacturer_title} добавлен'


@connection_to_DB
def db_get_all_manufacturers(cursor):
    """Получение всех производителей"""
    cursor.execute(
        """SELECT * FROM manufacturers"""
    )
    data = cursor.fetchall()
    data_dict = {item[0]: {'title': item[1], 'address': item[2]} for item in data}
    return data_dict


@connection_to_DB
def get_title_manufacturer(cursor, manufacturer_id: int):
    cursor.execute(
        """SELECT manufacturer_title FROM manufacturers
                                WHERE manufacturer_id = ?""",
        (manufacturer_id,)
    )
    return cursor.fetchone()[0]


@connection_to_DB
def db_add_product_without_barcode(cursor,
                                   product_name: str,
                                   price_product: float,
                                   weight_per_unit: float,
                                   manufacturer_id: int) -> str:
    """Добавление товара"""
    cursor.execute(
        """INSERT INTO products (product_name, price_product, weight_per_unit, manufacturer_id)
                               VALUES (?, ?, ?, ?)""",
        (product_name, price_product, weight_per_unit, manufacturer_id)
    )
    return f'Товар {product_name} добавлен'

