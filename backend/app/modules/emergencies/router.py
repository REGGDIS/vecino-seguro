"""Rutas HTTP para emergencias.

Este router solo coordina la entrada y salida HTTP. La lógica de negocio
queda en ``EmergencyService`` y el acceso a datos en ``EmergencyRepository``.
"""

from fastapi import APIRouter, HTTPException

from app.modules.emergencies.schemas import EmergencySummary
from app.modules.emergencies.service import EmergencyService

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

