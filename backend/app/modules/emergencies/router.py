"""Rutas HTTP para emergencias.

Este router solo coordina la entrada y salida HTTP. La lógica de negocio
queda en ``EmergencyService`` y el acceso a datos en ``EmergencyRepository``.
"""

from fastapi import APIRouter, HTTPException, status

from app.modules.emergencies.schemas import (
    EmergencyCatalogs,
    EmergencyCreate,
    EmergencySummary,
)
from app.modules.emergencies.service import (
    EmergencyService,
    EmergencyValidationError,
)

router = APIRouter()
emergency_service = EmergencyService()


@router.get("/", response_model=list[EmergencySummary])
def list_emergencies() -> list[EmergencySummary]:
    """Lista emergencias registradas en MySQL.

    Devuelve un arreglo JSON con las emergencias almacenadas, ordenadas por
    fecha de creación descendente. Si la base de datos no responde o la
    consulta falla, retorna ``500`` con un mensaje genérico para no exponer
    detalles internos del servidor.
    """
    try:
        return emergency_service.list_emergencies()
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="No fue posible obtener las emergencias",
        ) from exc


@router.get("/catalogs", response_model=EmergencyCatalogs)
def get_emergency_catalogs() -> EmergencyCatalogs:
    """Entrega catalogos fijos para formularios y filtros de emergencias."""
    return emergency_service.get_catalogs()


@router.post(
    "/",
    response_model=EmergencySummary,
    status_code=status.HTTP_201_CREATED,
)
def create_emergency(emergency_data: EmergencyCreate) -> EmergencySummary:
    """Crea una emergencia real en MySQL con estado inicial pendiente."""
    try:
        return emergency_service.create_emergency(emergency_data)
    except EmergencyValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="No fue posible crear la emergencia",
        ) from exc

