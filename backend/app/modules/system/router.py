"""Rutas de información general del sistema."""

from fastapi import APIRouter

from app.modules.system.schemas import SystemInfo
from app.modules.system.service import SystemService

router = APIRouter()
system_service = SystemService()


@router.get("/info", response_model=SystemInfo)
def get_system_info() -> SystemInfo:
    """Entrega información general del backend VecinoSeguro."""
    return system_service.get_info()