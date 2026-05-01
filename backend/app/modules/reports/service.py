"""Servicio de reportes.

Este módulo permitirá generar estadísticas y resúmenes de emergencias para
usuarios administradores o paneles de monitoreo.
"""

from app.modules.reports.repository import ReportRepository
from app.modules.reports.schemas import ReportSummary


class ReportService:
    """Coordina cálculos y consultas agregadas."""

    def __init__(self) -> None:
        self.repository = ReportRepository()

    def get_summary(self) -> ReportSummary:
        """Retorna métricas iniciales desde el repositorio."""
        return self.repository.get_summary()

