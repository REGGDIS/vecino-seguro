"""Controlador base para creación y listado de emergencias.

La lógica del controlador se mantiene independiente del toolkit visual para
facilitar el uso de PySide6 o Tkinter.
"""


class EmergencyController:
    """Coordina formularios y servicios relacionados con emergencias."""

    def list_emergencies(self) -> list[dict]:
        """Placeholder para cargar emergencias desde el backend."""
        return []

    def create_emergency(self, payload: dict) -> dict:
        """Placeholder para enviar una nueva emergencia al backend."""
        return payload
