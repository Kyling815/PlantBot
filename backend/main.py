"""
PlantBot FastAPI — main entry point.
Mounts all sub-routers and configures middleware.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.cnn_service.routes import router as cnn_router
from backend.agent.routes import router as agent_router
from backend.database.db import init_db

app = FastAPI(
    title="PlantBot API",
    description="AI-powered plant disease detection and treatment assistant",
    version="1.0.0",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(cnn_router, prefix="/api")
app.include_router(agent_router, prefix="/api")


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/")
def root():
    return {"message": "PlantBot API is running 🌿"}


@app.get("/health")
def health():
    return {"status": "ok"}
