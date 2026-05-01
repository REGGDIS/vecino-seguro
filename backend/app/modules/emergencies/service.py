"""Reglas de negocio para emergencias."""

from app.modules.emergencies.repository import EmergencyRepository
from app.modules.emergencies.schemas import EmergencySummary


class EmergencyService:
    """Coordina casos de uso para crear, listar y actualizar emergencias."""

    def __init__(self) -> None:
        self.repository = EmergencyRepository()

    def list_emergencies(self) -> list[EmergencySummary]:
        """Retorna emergencias desde el repositorio cuando exista persistencia."""
        return self.repository.list_emergencies()

