"""Controlador base para eventos de autenticación.

Este controlador no depende de PySide6 ni de Tkinter; su objetivo es coordinar
la interfaz desktop en Python con los servicios de la aplicación.
"""

from src.services.api_client import ApiClient


class AuthController:
    """Coordina la vista de login con servicios de autenticación."""

    def __init__(self, api_client: ApiClient | None = None) -> None:
        self.api_client = api_client or ApiClient()

    def login(self, rut: str, password: str) -> bool:
        """Placeholder para validar credenciales contra el backend."""
        return bool(rut.strip() and password.strip())
