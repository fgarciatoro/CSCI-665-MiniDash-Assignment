from typing import List

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.repository import MiniDashRepository
from app.services import MiniDashService

router = APIRouter()
service = MiniDashService(MiniDashRepository())


class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = Field(gt=0)


class OrderCreateRequest(BaseModel):
    restaurant_id: int
    address: str
    items: List[OrderItemCreate]


class OrderStatusUpdateRequest(BaseModel):
    status: str


@router.get("/restaurants")
def get_restaurants():
    return service.list_restaurants()


@router.get("/restaurants/{restaurant_id}/menu")
def get_restaurant_menu(restaurant_id: int):
    return service.get_menu(restaurant_id)


@router.post("/orders", status_code=201)
def create_order(request: OrderCreateRequest):
    return service.create_order(
        restaurant_id=request.restaurant_id,
        address=request.address,
        items=[item.model_dump() for item in request.items],
    )


@router.get("/orders/{order_id}")
def get_order(order_id: int):
    return service.get_order(order_id)


@router.patch("/orders/{order_id}/status")
def update_order_status(order_id: int, request: OrderStatusUpdateRequest):
    return service.update_order_status(order_id, request.status)
