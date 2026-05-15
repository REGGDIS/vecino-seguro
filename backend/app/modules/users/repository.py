"""Repositorio de usuarios.

Este archivo centralizará las operaciones de lectura y escritura de usuarios
en MySQL para evitar que la lógica de base de datos se mezcle con rutas o servicios.
"""

from typing import Any

from app.db.connection import get_connection
from app.modules.users.schemas import UserCreateResponse, UserSummary


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

    def find_by_email(self, email: str) -> dict[str, Any] | None:
        """Busca un usuario por email limpio."""
        query = """
            SELECT
                id,
                rut,
                full_name,
                email,
                password_hash,
                role_id
            FROM users
            WHERE email = %s
            LIMIT 1
        """
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, (email,))
            return cursor.fetchone()
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()

    def role_exists(self, role_id: int) -> bool:
        """Indica si el rol existe en la tabla roles."""
        query = "SELECT id FROM roles WHERE id = %s LIMIT 1"
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, (role_id,))
            return cursor.fetchone() is not None
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()

    def create_user(
        self,
        rut: str,
        full_name: str,
        email: str,
        password_hash: str,
        role_id: int,
    ) -> UserCreateResponse:
        """Inserta un usuario y retorna sus datos seguros."""
        insert_query = """
            INSERT INTO users (
                rut,
                full_name,
                email,
                password_hash,
                role_id
            )
            VALUES (%s, %s, %s, %s, %s)
        """
        select_query = """
            SELECT
                id,
                rut,
                full_name,
                email,
                role_id
            FROM users
            WHERE id = %s
            LIMIT 1
        """
        connection = get_connection()
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                insert_query,
                (rut, full_name, email, password_hash, role_id),
            )
            connection.commit()

            user_id = cursor.lastrowid
            cursor.execute(select_query, (user_id,))
            row = cursor.fetchone()
            if row is None:
                raise RuntimeError("No fue posible recuperar el usuario creado")

            return UserCreateResponse(**row)
        except Exception:
            try:
                connection.rollback()
            except Exception:
                pass
            raise
        finally:
            if cursor is not None:
                cursor.close()
            connection.close()
