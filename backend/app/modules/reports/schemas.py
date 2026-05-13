"""Modelos Pydantic para reportes."""

from pydantic import BaseModel


class ReportSummary(BaseModel):
    """Resumen agregado de emergencias."""

    total_emergencies: int
    open_emergencies: int
    resolved_emergencies: int


class ReportsSummaryResponse(BaseModel):
    """Resumen general de emergencias para dashboard."""

    total_emergencies: int
    by_status: dict[str, int]
    by_urgency: dict[str, int]


class DashboardCard(BaseModel):
    """Tarjeta simple para mostrar indicadores en dashboard."""

    key: str
    label: str
    value: int


class DashboardCardsResponse(BaseModel):
    """Respuesta con tarjetas de indicadores para dashboard."""

    cards: list[DashboardCard]