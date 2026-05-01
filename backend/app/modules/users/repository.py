"""Repositorio de usuarios.

Este archivo centralizará las operaciones de lectura y escritura de usuarios
en MySQL para evitar que la lógica de base de datos se mezcle con rutas o servicios.
"""

from app.modules.users.schemas import UserSummary


class UserRepository:
    """Repositorio inicial para la entidad usuario."""

    def list_users(self) -> list[UserSummary]:
        """Placeholder sin datos persistentes todavía."""
        return []

