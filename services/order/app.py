import os
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, generate_latest
from starlette.responses import Response

app = FastAPI(title="Order Service")
requests_total = Counter("order_requests_total", "Total requests for order service")
errors_total = Counter("order_errors_total", "Total errors in order service")
db_ready = Gauge(
    "order_service_db_ready",
    "1 if DB config is healthy (BROKEN_DB_CONFIG is false), else 0. Updated on each /metrics scrape.",
)
order_items = [
    {"order_id": 5001, "user_id": 100, "amount": 50.0},
    {"order_id": 5002, "user_id": 101, "amount": 75.5},
]


class OrderPayload(BaseModel):
    user_id: int
    amount: float


def db_config() -> dict[str, Any]:
    broken = os.getenv("BROKEN_DB_CONFIG", "false").lower() == "true"
    host = "invalid-db-host" if broken else os.getenv("DB_HOST", "postgres")
    return {
        "host": host,
        "port": int(os.getenv("DB_PORT", "5432")),
        "db_name": os.getenv("DB_NAME", "orders_db"),
        "user": os.getenv("DB_USER", "postgres"),
    }


def refresh_db_ready_gauge() -> None:
    cfg = db_config()
    db_ready.set(0.0 if cfg["host"] == "invalid-db-host" else 1.0)


@app.get("/health")
def health():
    requests_total.inc()
    cfg = db_config()
    if cfg["host"] == "invalid-db-host":
        errors_total.inc()
        raise HTTPException(status_code=500, detail="Database connection failed")
    return {"service": os.getenv("SERVICE_NAME", "order-service"), "status": "ok", "db_host": cfg["host"]}


@app.get("/orders")
def orders():
    requests_total.inc()
    cfg = db_config()
    if cfg["host"] == "invalid-db-host":
        errors_total.inc()
        raise HTTPException(status_code=500, detail="Cannot fetch orders: DB misconfigured")
    return order_items


@app.post("/orders")
def create_order(payload: OrderPayload):
    requests_total.inc()
    cfg = db_config()
    if cfg["host"] == "invalid-db-host":
        errors_total.inc()
        raise HTTPException(status_code=500, detail="Cannot create order: DB misconfigured")
    next_id = max(item["order_id"] for item in order_items) + 1 if order_items else 1
    item = {"order_id": next_id, "user_id": payload.user_id, "amount": payload.amount}
    order_items.append(item)
    return item


@app.get("/metrics")
def metrics():
    refresh_db_ready_gauge()
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
