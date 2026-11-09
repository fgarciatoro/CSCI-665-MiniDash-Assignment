import json
import os
import socket
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _request(base_url: str, method: str, path: str, payload=None):
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(f"{base_url}{path}", data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(request) as response:
            body = response.read().decode("utf-8")
            return response.getcode(), json.loads(body) if body else None
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8")
        parsed = json.loads(body) if body else None
        return error.code, parsed


@pytest.fixture
def api_server(tmp_path: Path):
    db_path = tmp_path / "test_minidash.db"
    port = _find_free_port()
    base_url = f"http://127.0.0.1:{port}"

    env = os.environ.copy()
    env["MINIDASH_DB_PATH"] = str(db_path)

    process = subprocess.Popen(
        ["python", "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", str(port)],
        cwd="/home/runner/work/CSCI-665-MiniDash-Assignment/CSCI-665-MiniDash-Assignment",
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    for _ in range(60):
        try:
            status, _ = _request(base_url, "GET", "/restaurants")
            if status == 200:
                break
        except Exception:
            pass
        time.sleep(0.1)
    else:
        process.terminate()
        process.wait(timeout=5)
        raise RuntimeError("API server did not start")

    yield base_url

    process.terminate()
    process.wait(timeout=5)


def test_get_restaurants_returns_seeded_data(api_server):
    status, data = _request(api_server, "GET", "/restaurants")

    assert status == 200
    assert len(data) == 5
    assert data[0]["name"] == "Pasta Palace"


def test_get_restaurant_menu_by_id(api_server):
    status, items = _request(api_server, "GET", "/restaurants/1/menu")

    assert status == 200
    assert len(items) >= 1
    assert all(item["restaurant_id"] == 1 for item in items)


def test_create_order_and_get_order(api_server):
    create_status, order = _request(
        api_server,
        "POST",
        "/orders",
        {
            "restaurant_id": 1,
            "address": "123 Main St",
            "items": [
                {"menu_item_id": 1, "quantity": 2},
                {"menu_item_id": 2, "quantity": 1},
            ],
        },
    )

    assert create_status == 201
    assert order["restaurant_id"] == 1
    assert order["status"] == "pending"
    assert order["total_cents"] == (1499 * 2) + 1299

    get_status, fetched_order = _request(api_server, "GET", f"/orders/{order['id']}")
    assert get_status == 200
    assert fetched_order["id"] == order["id"]
    assert len(fetched_order["items"]) == 2


def test_patch_order_status(api_server):
    create_status, created = _request(
        api_server,
        "POST",
        "/orders",
        {
            "restaurant_id": 2,
            "address": "45 Broadway",
            "items": [{"menu_item_id": 3, "quantity": 1}],
        },
    )
    assert create_status == 201

    patch_status, updated = _request(api_server, "PATCH", f"/orders/{created['id']}/status", {"status": "preparing"})

    assert patch_status == 200
    assert updated["status"] == "preparing"


def test_get_order_not_found(api_server):
    status, payload = _request(api_server, "GET", "/orders/9999")

    assert status == 404
    assert payload["detail"] == "Order not found"
