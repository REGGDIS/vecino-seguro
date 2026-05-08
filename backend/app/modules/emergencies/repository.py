"""Repositorio de emergencias.

Este módulo concentra el acceso a MySQL para la tabla ``emergencies``. La
capa de servicio y la capa HTTP no deben construir consultas SQL por su
cuenta: deben hacerlo siempre a través de este repositorio.
"""

from app.db.connection import get_connection
from app.modules.emergencies.schemas import EmergencySummary


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

