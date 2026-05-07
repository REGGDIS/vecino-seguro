"""Servicio de información general del sistema."""

from app.config.settings import settings
from app.modules.system.schemas import SystemInfo


class SystemService:
    """Entrega información general del backend."""

    def get_info(self) -> SystemInfo:
        """Retorna información básica del sistema."""
        return SystemInfo(
            app_name=settings.app_name,
            version="0.1.0",
            environment=settings.app_env,
            status="running",
            message="Backend VecinoSeguro operativo",
        )