from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import fraud, compare, report, health, monitoring  # Spending analysis endpoints
from backend.core.logging_config import setup_logging

app = FastAPI(title="Guard My Bills API", version="1.1.0")

# Allow all origins for local development
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)
setup_logging()

app.include_router(fraud.router)
app.include_router(compare.router)
app.include_router(report.router)
app.include_router(health.router)
app.include_router(monitoring.router)
