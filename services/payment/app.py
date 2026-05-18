import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from starlette.responses import Response

app = FastAPI(title="Payment Service")
requests_total = Counter("payment_requests_total", "Total requests for payment service")
errors_total = Counter("payment_errors_total", "Total errors in payment service")
payments = [
    {"payment_id": 9001, "order_id": 5001, "amount": 50.0, "status": "completed"},
    {"payment_id": 9002, "order_id": 5002, "amount": 75.5, "status": "completed"},
]


class PaymentPayload(BaseModel):
    order_id: int
    amount: float


@app.get("/health")
def health():
    requests_total.inc()
    return {"service": os.getenv("SERVICE_NAME", "payment-service"), "status": "ok"}


@app.get("/payments")
def list_payments():
    requests_total.inc()
    return payments


@app.post("/payments")
def process_payment(payload: PaymentPayload):
    requests_total.inc()
    if payload.amount <= 0:
        errors_total.inc()
        raise HTTPException(status_code=400, detail="Invalid payment amount")
    next_id = max(p["payment_id"] for p in payments) + 1 if payments else 1
    item = {
        "payment_id": next_id,
        "order_id": payload.order_id,
        "amount": payload.amount,
        "status": "completed",
    }
    payments.append(item)
    return item


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
