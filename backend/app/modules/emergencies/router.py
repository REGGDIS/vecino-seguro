"""Rutas base para reportes de emergencias."""

from fastapi import APIRouter

from app.modules.emergencies.schemas import EmergencySummary
from app.modules.emergencies.service import EmergencyService

router = APIRouter()
emergency_service = EmergencyService()


@router.get("/", response_model=list[EmergencySummary])
def list_emergencies() -> list[EmergencySummary]:
    """Ruta placeholder para consultar emergencias registradas."""
    return emergency_service.list_emergencies()

