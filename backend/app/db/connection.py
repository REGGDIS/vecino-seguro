"""Conexión centralizada a MySQL.

Este archivo deja preparada la creación del motor de SQLAlchemy. La conexión
real se activará cuando existan repositorios y modelos persistentes.
"""

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app.config.settings import settings


def create_database_engine() -> Engine:
    """Crea un motor SQLAlchemy para MySQL usando variables de entorno.

    La función no ejecuta consultas por sí sola. Los módulos de repositorio
    deberán usar este punto central para evitar conexiones dispersas.
    """
    return create_engine(settings.database_url, pool_pre_ping=True)

