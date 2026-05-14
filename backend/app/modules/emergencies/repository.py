"""Repositorio de emergencias.

Este módulo concentra el acceso a MySQL para la tabla ``emergencies``. La
capa de servicio y la capa HTTP no deben construir consultas SQL por su
cuenta: deben hacerlo siempre a través de este repositorio.
"""

from app.db.connection import get_connection
from app.modules.emergencies.schemas import EmergencyCreate, EmergencySummary


class EmergencyRepository:
    """Consulta emergencias almacenadas en MySQL."""

    def list_emergencies(self) -> list[EmergencySummary]:
        """Retorna todas las emergencias ordenadas por fecha descendente.

        Cierra el cursor y la conexión incluso si la consulta falla, para
        evitar fugas de conexiones cuando el endpoint reciba muchas
        peticiones.
        """
        query = """
            SELECT
                id,
                user_id,
                type,
                description,
                location,
                urgency_level,
                status,
                created_at,
                updated_at
            FROM emergencies
            ORDER BY created_at DESC
        """

        connection = get_connection()
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            rows = cursor.fetchall()
            return [EmergencySummary(**row) for row in rows]
        finally:
            if cursor is not None:
                cursor.close()
            connection.close()

    def update_status(self, emergency_id: int, status: str) -> EmergencySummary | None:
        """Actualiza estado y ``updated_at``; retorna la emergencia actualizada."""
        update_query = """
            UPDATE emergencies
            SET status = %s,
                updated_at = NOW()
            WHERE id = %s
        """
        select_query = """
            SELECT
                id,
                user_id,
                type,
                description,
                location,
                urgency_level,
                status,
                created_at,
                updated_at
            FROM emergencies
            WHERE id = %s
        """

        connection = get_connection()
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(update_query, (status, emergency_id))
            connection.commit()

            cursor.execute(select_query, (emergency_id,))
            row = cursor.fetchone()
            return EmergencySummary(**row) if row is not None else None
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

    def create_emergency(
        self,
        emergency_data: EmergencyCreate,
        status: str,
    ) -> EmergencySummary:
        """Inserta una emergencia y retorna el registro creado desde MySQL."""
        insert_query = """
            INSERT INTO emergencies (
                user_id,
                type,
                description,
                location,
                urgency_level,
                status
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        select_query = """
            SELECT
                id,
                user_id,
                type,
                description,
                location,
                urgency_level,
                status,
                created_at,
                updated_at
            FROM emergencies
            WHERE id = %s
        """

        connection = get_connection()
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                insert_query,
                (
                    emergency_data.user_id,
                    emergency_data.type,
                    emergency_data.description,
                    emergency_data.location,
                    emergency_data.urgency_level,
                    status,
                ),
            )
            connection.commit()

            emergency_id = cursor.lastrowid
            cursor.execute(select_query, (emergency_id,))
            row = cursor.fetchone()
            if row is None:
                raise RuntimeError("No fue posible recuperar la emergencia creada")

            return EmergencySummary(**row)
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

    def find_by_id(self, emergency_id: int) -> EmergencySummary | None:
        """Retorna una emergencia por ID o None si no existe."""
        query = """
            SELECT
                id,
                user_id,
                type,
                description,
                location,
                urgency_level,
                status,
                created_at,
                updated_at
            FROM emergencies
            WHERE id = %s
            LIMIT 1
        """

        connection = get_connection()
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, (emergency_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return EmergencySummary(**row)
        finally:
            if cursor is not None:
                cursor.close()
            connection.close()

