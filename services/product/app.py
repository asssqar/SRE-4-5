import os

from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from starlette.responses import Response

app = FastAPI(title="Product Service")
requests_total = Counter("product_requests_total", "Total requests for product service")
product_items = [
    {"id": 1, "name": "Keyboard", "price": 35.0},
    {"id": 2, "name": "Mouse", "price": 15.0},
]


class ProductPayload(BaseModel):
    name: str
    price: float


@app.get("/health")
def health():
    requests_total.inc()
    return {"service": os.getenv("SERVICE_NAME", "product-service"), "status": "ok"}


@app.get("/products")
def products():
    requests_total.inc()
    return product_items


@app.post("/products")
def create_product(payload: ProductPayload):
    requests_total.inc()
    next_id = max(item["id"] for item in product_items) + 1 if product_items else 1
    item = {"id": next_id, "name": payload.name, "price": payload.price}
    product_items.append(item)
    return item


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
