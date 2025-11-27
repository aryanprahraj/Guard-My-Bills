from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
import logging
import os

router = APIRouter(tags=["Monitoring"])

@router.get("/metrics", response_class=PlainTextResponse)
def metrics():
    # Simple Prometheus-style metrics example
    return "guardmybills_requests_total 1\n"

@router.get("/logs", response_class=PlainTextResponse)
def logs():
    log_path = os.getenv("GUARDMYBILLS_LOG_PATH", "app.log")
    if os.path.exists(log_path):
        with open(log_path) as f:
            return f.read()[-5000:]
    return "No logs found."
