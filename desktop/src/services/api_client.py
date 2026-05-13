"""Cliente HTTP base para comunicarse con el backend FastAPI."""

import requests

from src.config.settings import settings


class ApiClientError(RuntimeError):
    """Error controlado para fallas de comunicacion con el backend."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        detail: object | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.detail = detail


class ApiClient:
    """Encapsula llamadas HTTP para mantener separada la comunicación externa."""

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = (base_url or settings.api_base_url).rstrip("/")

    def health_check(self) -> dict:
        """Consulta el endpoint de salud del backend."""
        response = requests.get(f"{self.base_url}/health", timeout=10)
        response.raise_for_status()
        return response.json()

    def get_system_info(self) -> dict | None:
        """Obtiene información general del backend."""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/system/info", timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

    def get_emergencies(self) -> list[dict] | None:
        """Obtiene la lista de emergencias del backend."""
        try:
            return self._request_json("GET", "/api/v1/emergencies/")
        except ApiClientError:
            return None

    def get_emergency_catalogs(self) -> dict:
        """Obtiene los catalogos validos para registrar emergencias."""
        return self._request_json("GET", "/api/v1/emergencies/catalogs")

    def create_emergency(self, payload: dict) -> dict:
        """Crea una emergencia real en el backend FastAPI."""
        return self._request_json("POST", "/api/v1/emergencies/", json=payload)

    def update_emergency_status(self, emergency_id: int, payload: dict) -> dict:
        """Actualiza el estado de una emergencia real en el backend."""
        return self._request_json(
            "PATCH",
            f"/api/v1/emergencies/{emergency_id}/status",
            json=payload,
        )

    def _request_json(self, method: str, path: str, **kwargs) -> dict | list[dict]:
        """Ejecuta una peticion HTTP y traduce errores a mensajes de usuario."""
        url = f"{self.base_url}{path}"
        try:
            response = requests.request(method, url, timeout=10, **kwargs)
        except requests.Timeout as exc:
            raise ApiClientError(
                "No fue posible conectar con el backend. "
                "La solicitud agotó el tiempo de espera."
            ) from exc
        except requests.ConnectionError as exc:
            raise ApiClientError(
                "No fue posible conectar con el backend. "
                "Verifica que FastAPI esté en ejecución."
            ) from exc
        except requests.RequestException as exc:
            raise ApiClientError(
                "No fue posible conectar con el backend. "
                "Verifica que FastAPI esté en ejecución."
            ) from exc

        if response.status_code >= 400:
            detail = self._response_detail(response)
            message = self._message_for_status(response.status_code)
            raise ApiClientError(message, response.status_code, detail)

        try:
            return response.json()
        except ValueError as exc:
            raise ApiClientError(
                "El backend respondió con un formato no esperado."
            ) from exc

    def _response_detail(self, response: requests.Response) -> object | None:
        try:
            data = response.json()
        except ValueError:
            return response.text.strip() or None
        return data.get("detail") if isinstance(data, dict) else data

    def _message_for_status(self, status_code: int) -> str:
        if status_code in (400, 422):
            return "El backend rechazó la solicitud. Verifica los datos enviados."
        if status_code == 404:
            return "No se encontró el recurso solicitado en el backend."
        if status_code >= 500:
            return "El backend no pudo procesar la solicitud. Inténtalo nuevamente."
        return "No fue posible completar la solicitud al backend."

