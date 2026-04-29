import os

from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from starlette.responses import Response

app = FastAPI(title="User Service")
requests_total = Counter("user_requests_total", "Total requests for user service")
user_items = [
    {"id": 100, "name": "Alice"},
    {"id": 101, "name": "Bob"},
]


class UserPayload(BaseModel):
    name: str


@app.get("/health")
def health():
    requests_total.inc()
    return {"service": os.getenv("SERVICE_NAME", "user-service"), "status": "ok"}


@app.get("/users")
def users():
    requests_total.inc()
    return user_items


@app.post("/users")
def create_user(payload: UserPayload):
    requests_total.inc()
    next_id = max(item["id"] for item in user_items) + 1 if user_items else 1
    item = {"id": next_id, "name": payload.name}
    user_items.append(item)
    return item


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
