import os

from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from starlette.responses import Response

app = FastAPI(title="Chat Service")
requests_total = Counter("chat_requests_total", "Total requests for chat service")
chat_items = [
    {"user": "Alice", "message": "Hello"},
    {"user": "Bob", "message": "Hi"},
]


class MessagePayload(BaseModel):
    user: str
    message: str


@app.get("/health")
def health():
    requests_total.inc()
    return {"service": os.getenv("SERVICE_NAME", "chat-service"), "status": "ok"}


@app.get("/messages")
def messages():
    requests_total.inc()
    return chat_items


@app.post("/messages")
def create_message(payload: MessagePayload):
    requests_total.inc()
    item = {"user": payload.user, "message": payload.message}
    chat_items.append(item)
    return item


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
