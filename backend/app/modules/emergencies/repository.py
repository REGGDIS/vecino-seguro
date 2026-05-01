"""Repositorio de emergencias.

Este módulo se conectará a MySQL para registrar incidentes, consultar estados
y mantener separada la lógica de persistencia.
"""

from app.modules.emergencies.schemas import EmergencySummary


class EmergencyRepository:
    """Repositorio inicial para emergencias."""

    def list_emergencies(self) -> list[EmergencySummary]:
        """Placeholder sin emergencias persistidas todavía."""
        return []

