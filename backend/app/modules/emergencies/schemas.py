"""Modelos Pydantic para emergencias."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


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

