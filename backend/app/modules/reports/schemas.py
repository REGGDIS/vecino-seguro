"""Modelos Pydantic para reportes."""

from pydantic import BaseModel


class ReportSummary(BaseModel):
    """Resumen agregado de emergencias."""

    total_emergencies: int
    open_emergencies: int
    resolved_emergencies: int

