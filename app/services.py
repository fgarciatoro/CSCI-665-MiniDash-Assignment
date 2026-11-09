from typing import Dict, List

from fastapi import HTTPException

from app.repository import MiniDashRepository

ALLOWED_STATUSES = {"pending", "preparing", "out_for_delivery", "delivered", "cancelled"}


class MiniDashService:
    def __init__(self, repository: MiniDashRepository):
        self.repository = repository

    def list_restaurants(self) -> List[Dict]:
        return self.repository.list_restaurants()

    def get_menu(self, restaurant_id: int) -> List[Dict]:
        restaurant = self.repository.get_restaurant(restaurant_id)
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        return self.repository.list_menu_items(restaurant_id)

    def create_order(self, restaurant_id: int, address: str, items: List[Dict]) -> Dict:
        restaurant = self.repository.get_restaurant(restaurant_id)
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        if not items:
            raise HTTPException(status_code=400, detail="Order must include at least one item")

        requested_item_ids = [item["menu_item_id"] for item in items]
        menu_items = self.repository.get_menu_items_by_ids(requested_item_ids)
        menu_items_by_id = {item["id"]: item for item in menu_items}

        computed_items = []
        total_cents = 0

        for item in items:
            menu_item_id = item["menu_item_id"]
            quantity = item["quantity"]

            if quantity <= 0:
                raise HTTPException(status_code=400, detail="Quantity must be greater than zero")

            if menu_item_id not in menu_items_by_id:
                raise HTTPException(status_code=400, detail=f"Menu item {menu_item_id} does not exist")

            menu_item = menu_items_by_id[menu_item_id]
            if menu_item["restaurant_id"] != restaurant_id:
                raise HTTPException(
                    status_code=400,
                    detail=f"Menu item {menu_item_id} does not belong to restaurant {restaurant_id}",
                )

            item_price_cents = menu_item["price_cents"]
            computed_items.append(
                {
                    "menu_item_id": menu_item_id,
                    "quantity": quantity,
                    "item_price_cents": item_price_cents,
                }
            )
            total_cents += item_price_cents * quantity

        return self.repository.create_order(restaurant_id, address, computed_items, total_cents)

    def get_order(self, order_id: int) -> Dict:
        order = self.repository.get_order(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order

    def update_order_status(self, order_id: int, status: str) -> Dict:
        if status not in ALLOWED_STATUSES:
            raise HTTPException(status_code=400, detail="Invalid status")
        order = self.repository.update_order_status(order_id, status)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
