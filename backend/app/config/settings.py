"""Configuración central del backend.

Las variables se leen desde el entorno para evitar credenciales en el código.
El archivo `.env.example` documenta los nombres esperados para desarrollo.
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _get_bool(name: str, default: bool = False) -> bool:
    """Convierte una variable de entorno textual a booleano."""
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    """Valores de configuración usados por la aplicación."""

    app_name: str = os.getenv("APP_NAME", "VecinoSeguro")
    app_env: str = os.getenv("APP_ENV", "development")
    debug: bool = _get_bool("DEBUG", True)
    database_host: str = os.getenv("DATABASE_HOST", "localhost")
    database_port: int = int(os.getenv("DATABASE_PORT", "3306"))
    database_name: str = os.getenv("DATABASE_NAME", "vecino_seguro")
    database_user: str = os.getenv("DATABASE_USER", "root")
    database_password: str = os.getenv("DATABASE_PASSWORD", "change_me")
    secret_key: str = os.getenv("SECRET_KEY", "change_me")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    @property
    def database_url(self) -> str:
        """Construye la URL de conexión para MySQL sin abrir la conexión."""
        return (
            f"mysql+mysqlconnector://{self.database_user}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}/{self.database_name}"
        )


settings = Settings()

