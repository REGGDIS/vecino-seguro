"""Punto de entrada del backend VecinoSeguro.

Este módulo crea la instancia principal de FastAPI y registra rutas base.
Más adelante concentrará la carga de middlewares, manejadores de errores y
routers de cada módulo funcional.
"""

from fastapi import FastAPI

from app.config.settings import settings
from app.modules.auth.router import router as auth_router
from app.modules.emergencies.router import router as emergencies_router
from app.modules.reports.router import router as reports_router
from app.modules.users.router import router as users_router

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    version="0.1.0",
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
app.include_router(emergencies_router, prefix="/api/v1/emergencies", tags=["emergencies"])
app.include_router(reports_router, prefix="/api/v1/reports", tags=["reports"])


@app.get("/health")
def health_check() -> dict[str, str]:
    """Entrega un estado simple para comprobar que la API responde."""
    return {"status": "ok", "message": "Backend VecinoSeguro operativo"}

