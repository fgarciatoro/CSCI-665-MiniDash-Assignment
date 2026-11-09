from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.database import get_connection


class MiniDashRepository:
    def list_restaurants(self) -> List[Dict]:
        connection = get_connection()
        rows = connection.execute(
            """
            SELECT id, name, cuisine, opens_at, closes_at, avg_prep_minutes
            FROM restaurants
            ORDER BY id
            """
        ).fetchall()
        connection.close()
        return [dict(row) for row in rows]

    def get_restaurant(self, restaurant_id: int) -> Optional[Dict]:
        connection = get_connection()
        row = connection.execute(
            """
            SELECT id, name, cuisine, opens_at, closes_at, avg_prep_minutes
            FROM restaurants
            WHERE id = ?
            """,
            (restaurant_id,),
        ).fetchone()
        connection.close()
        return dict(row) if row else None

    def list_menu_items(self, restaurant_id: int) -> List[Dict]:
        connection = get_connection()
        rows = connection.execute(
            """
            SELECT id, restaurant_id, name, price_cents
            FROM menu_items
            WHERE restaurant_id = ?
            ORDER BY id
            """,
            (restaurant_id,),
        ).fetchall()
        connection.close()
        return [dict(row) for row in rows]

    def get_menu_items_by_ids(self, menu_item_ids: List[int]) -> List[Dict]:
        if not menu_item_ids:
            return []
        placeholders = ",".join("?" for _ in menu_item_ids)
        connection = get_connection()
        rows = connection.execute(
            f"""
            SELECT id, restaurant_id, name, price_cents
            FROM menu_items
            WHERE id IN ({placeholders})
            """,
            tuple(menu_item_ids),
        ).fetchall()
        connection.close()
        return [dict(row) for row in rows]

    def create_order(self, restaurant_id: int, address: str, items: List[Dict], total_cents: int) -> Dict:
        connection = get_connection()
        cursor = connection.cursor()
        created_at = datetime.now(timezone.utc).isoformat()

        cursor.execute(
            """
            INSERT INTO orders (restaurant_id, status, total_cents, address, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (restaurant_id, "pending", total_cents, address, created_at),
        )

        order_id = cursor.lastrowid

        cursor.executemany(
            """
            INSERT INTO order_items (order_id, menu_item_id, quantity, item_price_cents)
            VALUES (?, ?, ?, ?)
            """,
            [
                (order_id, item["menu_item_id"], item["quantity"], item["item_price_cents"])
                for item in items
            ],
        )

        connection.commit()
        connection.close()

        return self.get_order(order_id)

    def get_order(self, order_id: int) -> Optional[Dict]:
        connection = get_connection()
        order_row = connection.execute(
            """
            SELECT id, restaurant_id, status, total_cents, address, created_at
            FROM orders
            WHERE id = ?
            """,
            (order_id,),
        ).fetchone()

        if not order_row:
            connection.close()
            return None

        item_rows = connection.execute(
            """
            SELECT oi.menu_item_id, mi.name, oi.quantity, oi.item_price_cents
            FROM order_items oi
            JOIN menu_items mi ON mi.id = oi.menu_item_id
            WHERE oi.order_id = ?
            ORDER BY oi.id
            """,
            (order_id,),
        ).fetchall()
        connection.close()

        order = dict(order_row)
        order["items"] = [dict(item_row) for item_row in item_rows]
        return order

    def update_order_status(self, order_id: int, status: str) -> Optional[Dict]:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE orders
            SET status = ?
            WHERE id = ?
            """,
            (status, order_id),
        )
        connection.commit()
        updated = cursor.rowcount > 0
        connection.close()

        if not updated:
            return None
        return self.get_order(order_id)
