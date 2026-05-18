"""Controlador para el alta básica de usuarios desde desktop."""

from src.core.rut_validator import RutValidator
from src.services.api_client import ApiClient, ApiClientError


VALID_ROLE_IDS = {1, 2}


class UserController:
    """Valida datos mínimos y delega la creación real al backend."""

    def __init__(self, api_client: ApiClient | None = None) -> None:
        self._api = api_client or ApiClient()

    def crear_usuario(
        self,
        rut: str,
        full_name: str,
        email: str,
        password: str,
        role_id: int,
    ) -> tuple[bool, str, dict | None]:
        rut_limpio = rut.strip()
        nombre_limpio = full_name.strip()
        email_limpio = email.strip().lower()
        password_limpia = password.strip()

        if not rut_limpio:
            return False, "El RUT es obligatorio.", None
        if not RutValidator.es_valido(rut_limpio):
            return False, "RUT inválido. Verifique el dígito verificador.", None
        if not nombre_limpio:
            return False, "El nombre completo es obligatorio.", None
        if not email_limpio:
            return False, "El email es obligatorio.", None
        if "@" not in email_limpio:
            return False, "El email no tiene un formato válido.", None
        if not password_limpia:
            return False, "La contraseña inicial es obligatoria.", None
        if len(password_limpia) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres.", None
        if role_id not in VALID_ROLE_IDS:
            return False, "Debe seleccionar un rol válido.", None

        payload = {
            "rut": RutValidator.formatear(rut_limpio),
            "full_name": nombre_limpio,
            "email": email_limpio,
            "password": password_limpia,
            "role_id": role_id,
        }
        try:
            creado = self._api.create_user(payload)
            return True, "Usuario creado correctamente.", creado
        except ApiClientError as exc:
            return False, self._mensaje_api_error(exc), None

    def listar_usuarios(self) -> tuple[bool, str, list[dict]]:
        """Obtiene usuarios reales para el listado administrador."""
        usuarios = self._api.get_users()
        if not isinstance(usuarios, list):
            return False, "No fue posible cargar el listado de usuarios.", []
        return True, "", usuarios

    def _mensaje_api_error(self, exc: ApiClientError) -> str:
        if isinstance(exc.detail, str) and exc.detail:
            return exc.detail
        if exc.status_code == 409:
            return "Ya existe un usuario con ese RUT o email."
        return exc.message
