"""Controlador de autenticación.

Coordina la vista de login con los servicios y repositorios sin acoplarse
al toolkit visual (PySide6 / Tkinter). Mantiene la firma `login(rut, password)`
del controlador base y agrega lógica real de validación de RUT y verificación
de contraseña hasheada.

Cuando el backend esté disponible, este controlador podrá derivar la
autenticación a `ApiClient.login()` sin cambiar su API pública.
"""

from typing import Optional

from src.core.password_service import PasswordService
from src.core.rut_validator import RutValidator
from src.models.entities import Usuario
from src.repositories.user_repository import UserRepository
from src.services.api_client import ApiClient


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
        usuario = self._repo.find_by_rut(rut_formateado)
        if not usuario:
            return AuthResult(False, mensaje="Usuario no encontrado.")

        if not PasswordService.verificar(password, usuario.password_hash):
            return AuthResult(False, mensaje="Contraseña incorrecta.")

        self._sesion_actual = usuario
        return AuthResult(True, usuario=usuario, mensaje="Bienvenido")

    def logout(self) -> None:
        self._sesion_actual = None

    @property
    def usuario_actual(self) -> Optional[Usuario]:
        return self._sesion_actual
