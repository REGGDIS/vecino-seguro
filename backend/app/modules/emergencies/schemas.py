"""Modelos Pydantic para emergencias."""

from datetime import datetime

from pydantic import BaseModel


class EmergencySummary(BaseModel):
    """Resumen de una emergencia para listados y paneles."""

    id: int
    type: str
    description: str
    location: str
    urgency_level: str
    status: str
    created_at: datetime

