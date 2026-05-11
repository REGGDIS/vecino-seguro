"""Repositorio de usuarios.

Este archivo centralizará las operaciones de lectura y escritura de usuarios
en MySQL para evitar que la lógica de base de datos se mezcle con rutas o servicios.
"""

from typing import Any

from app.db.connection import get_connection
from app.modules.users.schemas import UserSummary


class UserRepository:
    """Repositorio inicial para la entidad usuario."""

    def list_users(self) -> list[UserSummary]:
        """Placeholder sin datos persistentes todavía."""
        return []

    def find_by_rut(self, rut: str) -> dict[str, Any] | None:
        """Busca un usuario por RUT normalizado."""
        query = """
            SELECT
                id,
                rut,
                full_name,
                email,
                password_hash,
                role_id
            FROM users
            WHERE rut = %s
            LIMIT 1
        """
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, (rut,))
            return cursor.fetchone()
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()
