"""Modelos Pydantic para emergencias."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CatalogOption(BaseModel):
    """Opcion disponible en un catalogo usado por emergencias."""

    value: str
    label: str


class EmergencyCatalogs(BaseModel):
    """Catalogos fijos para formularios y filtros de emergencias."""

    emergency_types: list[CatalogOption]
    urgency_levels: list[CatalogOption]
    statuses: list[CatalogOption]


class EmergencyCreate(BaseModel):
    """Datos requeridos para registrar una nueva emergencia."""

    user_id: int
    type: str
    description: str
    location: str
    urgency_level: str


class EmergencyStatusUpdate(BaseModel):
    """Datos para cambiar el estado de una emergencia.

    ``comment`` queda reservado para una futura issue de historial de estados;
    la tabla actual ``emergencies`` no persiste observaciones por cambio.
    """

    status: str
    comment: str | None = None


class EmergencySummary(BaseModel):
    """Resumen de una emergencia para listados y paneles.

    Representa la respuesta del endpoint ``GET /api/v1/emergencies`` con los
    campos almacenados en la tabla ``emergencies`` de MySQL. El campo
    ``updated_at`` es opcional porque puede ser ``NULL`` para registros muy
    antiguos sin fecha de actualización.
    """

    id: int
    user_id: int
    type: str
    description: str
    location: str
    urgency_level: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

