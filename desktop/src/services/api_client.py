"""Cliente HTTP base para comunicarse con el backend FastAPI."""

import logging
from typing import Any

import requests
from requests.exceptions import ConnectionError, RequestException, Timeout

from src.config.settings import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ApiClient:
    """Encapsula llamadas HTTP para mantener separada la comunicación externa."""

    API_PREFIX = "/api/v1"

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = (base_url or settings.api_base_url).rstrip("/")
        self.token: str | None = None
        self.last_error: str | None = None

    def _headers(self, authenticated: bool = False) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if authenticated and self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _build_url(self, path: str) -> str:
        return f"{self.base_url}{self.API_PREFIX}{path}"

    def _handle_response(
        self, response: requests.Response
    ) -> dict[str, Any] | list[dict] | None:
        try:
            data = response.json()
        except ValueError as exc:
            self.last_error = f"Respuesta no JSON del backend: {exc}"
            logger.error(self.last_error)
            return None

        if response.ok:
            self.last_error = None
            return data

        self.last_error = f"Backend respondió con estado {response.status_code}: {data}"
        logger.warning(self.last_error)
        return data

    def login(self, rut: str, password: str) -> dict | None:
        """POST /auth/login — retorna token y datos del usuario, o None si falla"""
        try:
            response = requests.post(
                self._build_url("/auth/login"),
                json={"rut": rut, "password": password},
                headers=self._headers(),
                timeout=10,
            )
            result = self._handle_response(response)
            if result is None:
                return None
            token = result.get("token")
            if token:
                self.token = token
            return result
        except (ConnectionError, Timeout) as exc:
            self.last_error = f"No se pudo conectar al backend en login: {exc}"
            logger.error(self.last_error)
            return None
        except RequestException as exc:
            self.last_error = f"Error en la petición de login: {exc}"
            logger.error(self.last_error)
            return None

    def listar_emergencias(self) -> list[dict]:
        """GET /emergencies — retorna lista, requiere Bearer token"""
        try:
            response = requests.get(
                self._build_url("/emergencies"),
                headers=self._headers(authenticated=True),
                timeout=10,
            )
            result = self._handle_response(response)
            if isinstance(result, list):
                return result
            return []
        except (ConnectionError, Timeout) as exc:
            self.last_error = f"No se pudo conectar al backend para listar emergencias: {exc}"
            logger.error(self.last_error)
            return []
        except RequestException as exc:
            self.last_error = f"Error en la petición de listado de emergencias: {exc}"
            logger.error(self.last_error)
            return []

    def obtener_emergencia(self, id: int) -> dict | None:
        """GET /emergencies/{id} — requiere Bearer token"""
        try:
            response = requests.get(
                self._build_url(f"/emergencies/{id}"),
                headers=self._headers(authenticated=True),
                timeout=10,
            )
            return self._handle_response(response)
        except (ConnectionError, Timeout) as exc:
            self.last_error = f"No se pudo conectar al backend para obtener emergencia {id}: {exc}"
            logger.error(self.last_error)
            return None
        except RequestException as exc:
            self.last_error = f"Error en la petición de obtener emergencia {id}: {exc}"
            logger.error(self.last_error)
            return None

    def crear_emergencia(self, payload: dict) -> dict | None:
        """POST /emergencies — requiere Bearer token"""
        try:
            response = requests.post(
                self._build_url("/emergencies"),
                json=payload,
                headers=self._headers(authenticated=True),
                timeout=10,
            )
            return self._handle_response(response)
        except (ConnectionError, Timeout) as exc:
            self.last_error = f"No se pudo conectar al backend para crear emergencia: {exc}"
            logger.error(self.last_error)
            return None
        except RequestException as exc:
            self.last_error = f"Error en la petición de crear emergencia: {exc}"
            logger.error(self.last_error)
            return None

    def cambiar_estado(
        self,
        id: int,
        nuevo_estado: str,
        observaciones: str = "",
    ) -> dict | None:
        """PATCH /emergencies/{id}/status — requiere Bearer token, solo admin"""
        try:
            response = requests.patch(
                self._build_url(f"/emergencies/{id}/status"),
                json={"estado": nuevo_estado, "observaciones": observaciones},
                headers=self._headers(authenticated=True),
                timeout=10,
            )
            return self._handle_response(response)
        except (ConnectionError, Timeout) as exc:
            self.last_error = f"No se pudo conectar al backend para cambiar estado de emergencia {id}: {exc}"
            logger.error(self.last_error)
            return None
        except RequestException as exc:
            self.last_error = f"Error en la petición de cambio de estado para emergencia {id}: {exc}"
            logger.error(self.last_error)
            return None

    def health_check(self) -> dict:
        """Consulta el endpoint de salud del backend."""
        response = requests.get(f"{self.base_url}/health", timeout=10)
        response.raise_for_status()
        return response.json()

