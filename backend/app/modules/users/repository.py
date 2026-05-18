"""Repositorio de usuarios.

Este archivo centralizará las operaciones de lectura y escritura de usuarios
en MySQL para evitar que la lógica de base de datos se mezcle con rutas o servicios.
"""

from typing import Any

from app.db.connection import get_connection
from app.modules.users.schemas import UserCreateResponse, UserListItem


class UserRepository:
    """Repositorio inicial para la entidad usuario."""

    def list_users(self) -> list[UserListItem]:
        """Lista usuarios reales con su rol, sin exponer credenciales."""
        query = """
            SELECT
                u.id,
                u.rut,
                u.full_name,
                u.email,
                u.role_id,
                r.name AS role,
                u.is_active
            FROM users u
            INNER JOIN roles r ON r.id = u.role_id
            ORDER BY u.id ASC
        """
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            rows = cursor.fetchall()
            return [UserListItem(**row) for row in rows]
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()

    def find_by_rut(self, rut: str) -> dict[str, Any] | None:
        """Busca un usuario por RUT normalizado."""
        query = """
            SELECT
                id,
                rut,
                full_name,
                email,
                password_hash,
                role_id,
                is_active
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
                role_id,
                is_active
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

    def find_by_id(self, user_id: int) -> dict[str, Any] | None:
        """Busca un usuario por ID sin retornar contraseña ni hash."""
        query = """
            SELECT
                id,
                rut,
                full_name,
                email,
                role_id,
                is_active
            FROM users
            WHERE id = %s
            LIMIT 1
        """
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, (user_id,))
            return cursor.fetchone()
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()

    def find_by_email_excluding_user(
        self,
        email: str,
        user_id: int,
    ) -> dict[str, Any] | None:
        """Busca un email que pertenezca a otro usuario."""
        query = """
            SELECT
                id,
                rut,
                full_name,
                email,
                role_id,
                is_active
            FROM users
            WHERE email = %s
              AND id <> %s
            LIMIT 1
        """
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, (email, user_id))
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

    def count_active_admins(self) -> int:
        """Cuenta administradores activos para proteger acceso al sistema."""
        query = """
            SELECT COUNT(*) AS total
            FROM users
            WHERE role_id = 1
              AND is_active = 1
        """
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            row = cursor.fetchone()
            return int(row["total"]) if row else 0
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
                role_id,
                is_active
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

    def update_active_status(
        self,
        user_id: int,
        is_active: bool,
    ) -> UserListItem | None:
        """Actualiza el estado activo/inactivo y retorna el usuario seguro."""
        update_query = """
            UPDATE users
            SET is_active = %s
            WHERE id = %s
        """
        select_query = """
            SELECT
                u.id,
                u.rut,
                u.full_name,
                u.email,
                u.role_id,
                r.name AS role,
                u.is_active
            FROM users u
            INNER JOIN roles r ON r.id = u.role_id
            WHERE u.id = %s
            LIMIT 1
        """
        connection = get_connection()
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(update_query, (1 if is_active else 0, user_id))
            connection.commit()

            cursor.execute(select_query, (user_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return UserListItem(**row)
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

    def update_user(
        self,
        user_id: int,
        full_name: str,
        email: str,
        role_id: int,
    ) -> UserListItem | None:
        """Actualiza datos básicos y retorna el usuario seguro actualizado."""
        update_query = """
            UPDATE users
            SET full_name = %s,
                email = %s,
                role_id = %s
            WHERE id = %s
        """
        select_query = """
            SELECT
                u.id,
                u.rut,
                u.full_name,
                u.email,
                u.role_id,
                r.name AS role,
                u.is_active
            FROM users u
            INNER JOIN roles r ON r.id = u.role_id
            WHERE u.id = %s
            LIMIT 1
        """
        connection = get_connection()
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(update_query, (full_name, email, role_id, user_id))
            connection.commit()

            cursor.execute(select_query, (user_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return UserListItem(**row)
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
