from fastapi import FastAPI

from app.api.routes.status_routes import router as status_router
from app.api.routes.camera_routes import router as camera_router

app = FastAPI(
    title="İnşaat Takip API",
    description="Raspberry Pi İnşaat Takip Sistemi API",
    version="1.0.0"
)


# ==================================================
# ROUTES
# ==================================================

app.include_router(
    status_router
)

app.include_router(
    camera_router
)