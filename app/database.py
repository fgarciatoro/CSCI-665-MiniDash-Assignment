import os
import sqlite3
from typing import Optional

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "minidash.db")


def get_db_path() -> str:
    return os.environ.get("MINIDASH_DB_PATH", DEFAULT_DB_PATH)


def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    connection = sqlite3.connect(db_path or get_db_path(), check_same_thread=False)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db(db_path: Optional[str] = None) -> None:
    connection = get_connection(db_path)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            cuisine TEXT NOT NULL,
            opens_at TEXT NOT NULL,
            closes_at TEXT NOT NULL,
            avg_prep_minutes INTEGER NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            price_cents INTEGER NOT NULL,
            FOREIGN KEY (restaurant_id) REFERENCES restaurants (id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            total_cents INTEGER NOT NULL,
            address TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (restaurant_id) REFERENCES restaurants (id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            menu_item_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            item_price_cents INTEGER NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (id),
            FOREIGN KEY (menu_item_id) REFERENCES menu_items (id)
        )
        """
    )

    cursor.execute("SELECT COUNT(*) AS count FROM restaurants")
    restaurant_count = cursor.fetchone()["count"]

    if restaurant_count == 0:
        restaurants = [
            ("Pasta Palace", "Italian", "10:00", "22:00", 20),
            ("Sushi Station", "Japanese", "11:00", "21:00", 25),
            ("Taco Town", "Mexican", "09:00", "23:00", 15),
            ("Curry Corner", "Indian", "10:30", "22:30", 30),
            ("Burger Barn", "American", "08:00", "00:00", 12),
        ]

        cursor.executemany(
            """
            INSERT INTO restaurants (name, cuisine, opens_at, closes_at, avg_prep_minutes)
            VALUES (?, ?, ?, ?, ?)
            """,
            restaurants,
        )

        menu_items = [
            (1, "Spaghetti Carbonara", 1499),
            (1, "Margherita Pizza", 1299),
            (2, "California Roll", 899),
            (2, "Salmon Nigiri", 1099),
            (3, "Chicken Taco", 399),
            (3, "Beef Burrito", 999),
            (4, "Chicken Tikka Masala", 1399),
            (4, "Garlic Naan", 299),
            (5, "Classic Cheeseburger", 1199),
            (5, "Fries", 399),
        ]

        cursor.executemany(
            """
            INSERT INTO menu_items (restaurant_id, name, price_cents)
            VALUES (?, ?, ?)
            """,
            menu_items,
        )

    connection.commit()
    connection.close()
