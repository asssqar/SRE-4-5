import os

from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from starlette.responses import Response

app = FastAPI(title="Auth Service")
requests_total = Counter("auth_requests_total", "Total requests for auth service")

class LoginPayload(BaseModel):
    username: str
    password: str


@app.get("/health")
def health():
    requests_total.inc()
    return {"service": os.getenv("SERVICE_NAME", "auth-service"), "status": "ok"}


@app.get("/login")
def login():
    requests_total.inc()
    return {"token": "mock-jwt-token", "role": "user"}

@app.post("/login")
def login_with_credentials(payload: LoginPayload):
    requests_total.inc()
    return {"token": f"mock-token-for-{payload.username}", "role": "user"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
