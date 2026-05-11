"""Rutas para reportes y métricas agregadas."""

from fastapi import APIRouter

from app.modules.reports.schemas import ReportsSummaryResponse
from app.modules.reports.service import ReportService

router = APIRouter()
report_service = ReportService()


@router.get("/summary", response_model=ReportsSummaryResponse)
def get_summary() -> ReportsSummaryResponse:
    """Entrega estadísticas agregadas de emergencias."""
    return report_service.get_summary()