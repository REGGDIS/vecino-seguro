"""Controlador de autenticación.

Coordina la vista de login con el backend real sin acoplarse al toolkit visual
PySide6. Mantiene la firma `login(rut, password)` del controlador base y agrega
un resultado detallado para que la vista muestre mensajes claros.
"""

from typing import Optional

from src.core.rut_validator import RutValidator
from src.models.entities import Rol, Usuario
from src.repositories.user_repository import UserRepository
from src.services.api_client import ApiClient, ApiClientError


class AuthResult:
    """Resultado detallado de un intento de autenticación."""

    def __init__(self, exito: bool, usuario: Optional[Usuario] = None,
                 mensaje: str = "") -> None:
        self.exito = exito
        self.usuario = usuario
        self.mensaje = mensaje


class AuthController:
    """Coordina la vista de login con los servicios de autenticación."""

    def __init__(
        self,
        user_repository: UserRepository | None = None,
        api_client: ApiClient | None = None,
    ) -> None:
        self._repo = user_repository or UserRepository()
        self.api_client = api_client or ApiClient()
        self._sesion_actual: Optional[Usuario] = None

    def login(self, rut: str, password: str) -> bool:
        """Mantiene la firma booleana del controlador base.

        Para obtener detalles del intento (mensaje, usuario autenticado),
        utilizar `login_detallado`.
        """
        return self.login_detallado(rut, password).exito

    def login_detallado(self, rut: str, password: str) -> AuthResult:
        if not rut.strip() or not password.strip():
            return AuthResult(False, mensaje="Complete todos los campos.")

        if not RutValidator.es_valido(rut):
            return AuthResult(
                False, mensaje="RUT inválido. Verifique el dígito verificador."
            )

        rut_formateado = RutValidator.formatear(rut)
        try:
            respuesta = self.api_client.login(rut_formateado, password)
            usuario = self._usuario_desde_backend(respuesta)
        except ApiClientError as exc:
            return AuthResult(False, mensaje=self._mensaje_error_login(exc))
        except (KeyError, TypeError, ValueError):
            return AuthResult(
                False,
                mensaje=(
                    "El backend respondió correctamente, pero no fue posible "
                    "interpretar los datos del usuario."
                ),
            )

        self._sesion_actual = usuario
        return AuthResult(True, usuario=usuario, mensaje="Bienvenido")

    def _usuario_desde_backend(self, respuesta: dict) -> Usuario:
        if not isinstance(respuesta, dict) or respuesta.get("success") is False:
            raise ValueError("respuesta de login inválida")

        datos = respuesta["user"]
        rol = self._rol_desde_backend(datos.get("role_id"))

        return Usuario(
            id=self._int_opcional(datos.get("id")),
            rut=RutValidator.formatear(datos.get("rut", "")),
            nombre=datos.get("full_name", ""),
            email=datos.get("email", ""),
            rol=rol,
            password_hash="",
            direccion="",
        )

    def _rol_desde_backend(self, role_id: object) -> Rol:
        try:
            return Rol.ADMIN if int(role_id) == 1 else Rol.VECINO
        except (TypeError, ValueError):
            return Rol.VECINO

    def _int_opcional(self, valor: object) -> int | None:
        if valor in (None, ""):
            return None
        try:
            return int(valor)
        except (TypeError, ValueError):
            return None

    def _mensaje_error_login(self, exc: ApiClientError) -> str:
        if exc.status_code == 401:
            return "RUT o contraseña incorrectos."
        if exc.status_code in (400, 422):
            return "Revise el formato del RUT y la contraseña."
        if exc.status_code is None:
            return exc.message
        if exc.status_code >= 500:
            return "El backend no pudo iniciar sesión. Inténtalo nuevamente."
        return exc.message

    def logout(self) -> None:
        self._sesion_actual = None

    @property
    def usuario_actual(self) -> Optional[Usuario]:
        return self._sesion_actual
