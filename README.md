# MiniDash

MiniDash is a small food-delivery REST API built with FastAPI and SQLite.

## Requirements

- Python 3.10+
- `fastapi`
- `uvicorn`
- `pytest`

## Run the API

From the repository root:

```bash
python -m uvicorn main:app --reload
```

API endpoints:
- `GET /restaurants`
- `GET /restaurants/{id}/menu`
- `POST /orders`
- `GET /orders/{id}`
- `PATCH /orders/{id}/status`

## Run tests

```bash
pytest
```

## Data model
SQLite tables:

- `restaurants (id, name, cuisine, opens_at, closes_at, avg_prep_minutes)`
- `menu_items (id, restaurant_id, name, price_cents)`
- `orders (id, restaurant_id, status, total_cents, address, created_at)`
- `order_items`

The database is initialized automatically on startup, including seed data for 5 restaurants.
