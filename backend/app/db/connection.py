"""Conexión centralizada a MySQL.

Este archivo expone dos puntos de acceso a la base de datos:

* ``get_connection``: conexión directa con ``mysql.connector`` para los
  repositorios actuales que ejecutan SQL plano.
* ``create_database_engine``: motor de SQLAlchemy preparado para módulos
  futuros que requieran un ORM o pool de conexiones más completo.

Los módulos deben usar este archivo como única capa de acceso a MySQL para
evitar conexiones dispersas en distintos puntos del backend.
"""

import mysql.connector
from mysql.connector.connection import MySQLConnection
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app.config.settings import settings


def get_connection() -> MySQLConnection:
    """Crea y retorna una conexión a MySQL usando variables de entorno.

    La conexión se construye con los datos definidos en ``.env`` y leídos
    por ``settings``. El llamador es responsable de cerrarla con
    ``connection.close()`` cuando termine de usarla.
    """
    return mysql.connector.connect(
        host=settings.database_host,
        port=settings.database_port,
        database=settings.database_name,
        user=settings.database_user,
        password=settings.database_password,
    )


def create_database_engine() -> Engine:
    """Crea un motor SQLAlchemy para MySQL usando variables de entorno.

    La función no ejecuta consultas por sí sola. Los módulos de repositorio
    que requieran SQLAlchemy deberán usar este punto central para evitar
    conexiones dispersas.
    """
    return create_engine(settings.database_url, pool_pre_ping=True)

