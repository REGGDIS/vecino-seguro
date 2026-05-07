"""Configuración inicial para la aplicación desktop."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _get_bool(name: str, default: bool = True) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class DesktopSettings:
    """Valores configurables de la app de escritorio."""

    app_name: str = os.getenv("DESKTOP_APP_NAME", "VecinoSeguro Desktop")
    api_base_url: str = os.getenv("API_BASE_URL", "http://localhost:8000")
    use_backend: bool = _get_bool("USE_BACKEND", False)


settings = DesktopSettings()

