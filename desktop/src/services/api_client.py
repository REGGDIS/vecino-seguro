"""Cliente HTTP base para comunicarse con el backend FastAPI."""

import requests

from src.config.settings import settings


class ApiClient:
    """Encapsula llamadas HTTP para mantener separada la comunicación externa."""

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = (base_url or settings.api_base_url).rstrip("/")

    def health_check(self) -> dict:
        """Consulta el endpoint de salud del backend."""
        response = requests.get(f"{self.base_url}/health", timeout=10)
        response.raise_for_status()
        return response.json()

