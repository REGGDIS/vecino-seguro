"""Rutas base para reportes y métricas."""

from fastapi import APIRouter

from app.modules.reports.schemas import ReportSummary
from app.modules.reports.service import ReportService

router = APIRouter()
report_service = ReportService()


@router.get("/summary", response_model=ReportSummary)
def get_summary() -> ReportSummary:
    """Entrega un resumen inicial sin datos reales todavía."""
    return report_service.get_summary()

