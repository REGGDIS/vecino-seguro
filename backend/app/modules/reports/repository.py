"""Repositorio para consultas agregadas y reportes."""

from app.modules.reports.schemas import ReportSummary


class ReportRepository:
    """Repositorio inicial para estadísticas."""

    def get_summary(self) -> ReportSummary:
        """Placeholder con contadores en cero hasta conectar MySQL."""
        return ReportSummary(total_emergencies=0, open_emergencies=0, resolved_emergencies=0)

