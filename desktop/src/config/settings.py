"""Configuración inicial para la aplicación desktop."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class DesktopSettings:
    """Valores configurables de la app de escritorio."""

    app_name: str = os.getenv("DESKTOP_APP_NAME", "VecinoSeguro Desktop")
    api_base_url: str = os.getenv("API_BASE_URL", "http://localhost:8000")


settings = DesktopSettings()

