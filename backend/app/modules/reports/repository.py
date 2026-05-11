"""Repositorio para consultas agregadas y reportes."""

from app.db.connection import get_connection


class ReportRepository:
    """Repositorio para estadísticas y reportes."""

    def get_total_emergencies(self) -> int:
        """Obtiene el total de emergencias registradas."""
        connection = get_connection()
        cursor = connection.cursor()

        query = "SELECT COUNT(*) FROM emergencies"
        cursor.execute(query)

        total = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return total

    def get_emergencies_by_status(self) -> dict[str, int]:
        """Obtiene conteo de emergencias agrupadas por estado."""
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT status, COUNT(*)
            FROM emergencies
            GROUP BY status
        """

        cursor.execute(query)

        results = cursor.fetchall()

        cursor.close()
        connection.close()

        return {status: count for status, count in results}

    def get_emergencies_by_urgency(self) -> dict[str, int]:
        """Obtiene conteo de emergencias agrupadas por urgencia."""
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT urgency_level, COUNT(*)
            FROM emergencies
            GROUP BY urgency_level
        """

        cursor.execute(query)

        results = cursor.fetchall()

        cursor.close()
        connection.close()

        return {urgency: count for urgency, count in results}