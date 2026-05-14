"""Servicio de reportes y estadísticas agregadas."""

from app.modules.reports.repository import ReportRepository
from app.modules.reports.schemas import (
    DashboardCard,
    DashboardCardsResponse,
    ReportsSummaryResponse,
)


class ReportService:
    """Coordina consultas y resúmenes estadísticos."""

    VALID_STATUSES = ["pendiente", "en_revision", "resuelto"]
    VALID_URGENCY_LEVELS = ["baja", "media", "alta", "critica"]

    def __init__(self) -> None:
        self.repository = ReportRepository()

    def get_summary(self) -> ReportsSummaryResponse:
        """Obtiene resumen agregado de emergencias."""

        total_emergencies = self.repository.get_total_emergencies()

        by_status = self.repository.get_emergencies_by_status()
        by_urgency = self.repository.get_emergencies_by_urgency()

        normalized_status = {
            status: by_status.get(status, 0)
            for status in self.VALID_STATUSES
        }

        normalized_urgency = {
            urgency: by_urgency.get(urgency, 0)
            for urgency in self.VALID_URGENCY_LEVELS
        }

        return ReportsSummaryResponse(
            total_emergencies=total_emergencies,
            by_status=normalized_status,
            by_urgency=normalized_urgency,
        )

    def get_dashboard_cards(self) -> DashboardCardsResponse:
        """Retorna indicadores preparados como tarjetas para dashboard."""

        summary = self.get_summary()

        return DashboardCardsResponse(
            cards=[
                DashboardCard(
                    key="total",
                    label="Emergencias totales",
                    value=summary.total_emergencies,
                ),
                DashboardCard(
                    key="pendiente",
                    label="Pendientes",
                    value=summary.by_status.get("pendiente", 0),
                ),
                DashboardCard(
                    key="en_revision",
                    label="En revisión",
                    value=summary.by_status.get("en_revision", 0),
                ),
                DashboardCard(
                    key="resuelto",
                    label="Resueltas",
                    value=summary.by_status.get("resuelto", 0),
                ),
                DashboardCard(
                    key="critica",
                    label="Urgencia crítica",
                    value=summary.by_urgency.get("critica", 0),
                ),
            ]
        )