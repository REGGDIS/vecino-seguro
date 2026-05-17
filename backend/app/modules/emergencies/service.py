"""Reglas de negocio para emergencias."""

from app.modules.emergencies.repository import EmergencyRepository
from app.modules.emergencies.schemas import (
    EmergencyCatalogs,
    EmergencyCreate,
    EmergencyStatusUpdate,
    EmergencySummary,
    EmergencySummaryStats,
)


EMERGENCY_TYPES = [
    {"value": "robo", "label": "Robo"},
    {"value": "incendio", "label": "Incendio"},
    {"value": "accidente", "label": "Accidente"},
    {"value": "emergencia_medica", "label": "Emergencia médica"},
    {"value": "corte_luz", "label": "Corte de luz"},
    {"value": "persona_extraviada", "label": "Persona extraviada"},
    {"value": "solicitud_ayuda", "label": "Solicitud de ayuda"},
    {"value": "otro", "label": "Otro"},
]

URGENCY_LEVELS = [
    {"value": "baja", "label": "Baja"},
    {"value": "media", "label": "Media"},
    {"value": "alta", "label": "Alta"},
    {"value": "critica", "label": "Crítica"},
]

STATUSES = [
    {"value": "pendiente", "label": "Pendiente"},
    {"value": "en_revision", "label": "En revisión"},
    {"value": "resuelto", "label": "Resuelto"},
]

INITIAL_STATUS = "pendiente"
VALID_STATUSES = {option["value"] for option in STATUSES}


class EmergencyValidationError(ValueError):
    """Error de validacion de reglas de negocio de emergencias."""


class EmergencyNotFoundError(LookupError):
    """Error cuando una emergencia solicitada no existe."""


class EmergencyService:
    """Coordina casos de uso para crear, listar y actualizar emergencias."""

    def __init__(self) -> None:
        self.repository = EmergencyRepository()

    def list_emergencies(self) -> list[EmergencySummary]:
        """Retorna emergencias desde el repositorio cuando exista persistencia."""
        return self.repository.list_emergencies()

    def get_summary(self) -> EmergencySummaryStats:
        """Retorna contadores agregados por estado."""
        return self.repository.get_summary()

    def list_recent(self, limit: int = 4) -> list[EmergencySummary]:
        """Retorna emergencias recientes con un limite acotado."""
        safe_limit = max(1, min(limit, 20))
        return self.repository.list_recent(safe_limit)

    def get_catalogs(self) -> EmergencyCatalogs:
        """Retorna catalogos fijos sin consultar la base de datos."""
        return EmergencyCatalogs(
            emergency_types=EMERGENCY_TYPES,
            urgency_levels=URGENCY_LEVELS,
            statuses=STATUSES,
        )

    def create_emergency(
        self,
        emergency_data: EmergencyCreate,
    ) -> EmergencySummary:
        """Valida y registra una emergencia con estado inicial pendiente."""
        self._validate_required_fields(emergency_data)
        self._validate_catalog_values(emergency_data)

        return self.repository.create_emergency(
            emergency_data=emergency_data,
            status=INITIAL_STATUS,
        )

    def get_emergency_by_id(self, emergency_id: int) -> EmergencySummary | None:
        """Obtiene una emergencia específica por ID."""
        return self.repository.find_by_id(emergency_id)

    def update_status(
        self,
        emergency_id: int,
        status_data: EmergencyStatusUpdate,
    ) -> EmergencySummary:
        """Valida y persiste el nuevo estado de una emergencia."""
        status = status_data.status.strip() if status_data.status else ""
        if status not in VALID_STATUSES:
            raise EmergencyValidationError(
                "Estado no valido. Use: pendiente, en_revision o resuelto"
            )

        updated = self.repository.update_status(emergency_id, status)
        if updated is None:
            raise EmergencyNotFoundError("Emergencia no encontrada")

        return updated

    def delete_emergency(self, emergency_id: int) -> None:
        """Elimina una emergencia existente."""
        deleted = self.repository.delete_by_id(emergency_id)
        if not deleted:
            raise EmergencyNotFoundError("Emergencia no encontrada")

    def _validate_required_fields(self, emergency_data: EmergencyCreate) -> None:
        if emergency_data.user_id is None:
            raise EmergencyValidationError("El usuario es obligatorio")

        required_text_fields = {
            "type": "El tipo de emergencia es obligatorio",
            "description": "La descripcion es obligatoria",
            "location": "La ubicacion es obligatoria",
            "urgency_level": "El nivel de urgencia es obligatorio",
        }

        for field_name, message in required_text_fields.items():
            value = getattr(emergency_data, field_name)
            if not value or not value.strip():
                raise EmergencyValidationError(message)

    def _validate_catalog_values(self, emergency_data: EmergencyCreate) -> None:
        valid_types = {option["value"] for option in EMERGENCY_TYPES}
        valid_urgency_levels = {option["value"] for option in URGENCY_LEVELS}

        if emergency_data.type not in valid_types:
            raise EmergencyValidationError("El tipo de emergencia no es valido")

        if emergency_data.urgency_level not in valid_urgency_levels:
            raise EmergencyValidationError("El nivel de urgencia no es valido")
