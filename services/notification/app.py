import os

from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from starlette.responses import Response

app = FastAPI(title="Notification Service")
requests_total = Counter("notification_requests_total", "Total requests for notification service")
notifications = [
    {"id": 1, "channel": "email", "recipient": "alice@example.com", "message": "Order confirmed"},
    {"id": 2, "channel": "email", "recipient": "bob@example.com", "message": "Payment received"},
]


class NotificationPayload(BaseModel):
    channel: str
    recipient: str
    message: str


@app.get("/health")
def health():
    requests_total.inc()
    return {"service": os.getenv("SERVICE_NAME", "notification-service"), "status": "ok"}


@app.get("/notifications")
def list_notifications():
    requests_total.inc()
    return notifications


@app.post("/notifications")
def send_notification(payload: NotificationPayload):
    requests_total.inc()
    next_id = max(n["id"] for n in notifications) + 1 if notifications else 1
    item = {
        "id": next_id,
        "channel": payload.channel,
        "recipient": payload.recipient,
        "message": payload.message,
        "status": "sent",
    }
    notifications.append(item)
    return item


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
