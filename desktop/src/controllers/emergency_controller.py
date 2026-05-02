"""Controlador base para creación y listado de emergencias.

La lógica del controlador se mantiene separada de las vistas PySide6 para que
los servicios y reglas de negocio no dependan directamente de la interfaz.
"""


class EmergencyController:
    """Coordina formularios y servicios relacionados con emergencias."""

    def list_emergencies(self) -> list[dict]:
        """Placeholder para cargar emergencias desde el backend."""
        return []

    def create_emergency(self, payload: dict) -> dict:
        """Placeholder para enviar una nueva emergencia al backend."""
        return payload
