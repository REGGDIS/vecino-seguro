"""Servicio de reportes y estadísticas agregadas."""

from app.modules.reports.repository import ReportRepository
from app.modules.reports.schemas import ReportsSummaryResponse


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