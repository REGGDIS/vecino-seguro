"""Servicio de autenticación."""

from passlib.context import CryptContext
from passlib.exc import UnknownHashError

from app.modules.auth.schemas import AuthenticatedUser, LoginResponse
from app.modules.users.repository import UserRepository
from app.shared.validators.rut_validator import normalize_rut, validate_rut


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class InvalidLoginDataError(Exception):
    """Indica que los datos de login no tienen formato válido."""


class InvalidCredentialsError(Exception):
    """Indica que las credenciales no corresponden a un usuario válido."""


class AuthService:
    """Servicio responsable de reglas de negocio del módulo de autenticación."""

    def __init__(self) -> None:
        self.user_repository = UserRepository()

    def validate_login_request(self, rut: str, password: str) -> bool:
        """Valida datos mínimos antes de intentar autenticar contra la base."""
        return bool(rut and password and password.strip() and validate_rut(rut))

    def login(self, rut: str, password: str) -> LoginResponse:
        """Autentica un usuario por RUT y contraseña."""
        if not self.validate_login_request(rut, password):
            raise InvalidLoginDataError

        normalized_rut = normalize_rut(rut)
        user = self.user_repository.find_by_rut(normalized_rut)
        if user is None:
            raise InvalidCredentialsError

        if not bool(user.get("is_active", True)):
            raise InvalidCredentialsError

        password_hash = user.get("password_hash")
        if not password_hash:
            raise InvalidCredentialsError

        try:
            password_matches = pwd_context.verify(password, password_hash)
        except (UnknownHashError, ValueError, TypeError):
            raise InvalidCredentialsError from None

        if not password_matches:
            raise InvalidCredentialsError

        authenticated_user = AuthenticatedUser(
            id=user["id"],
            rut=user["rut"],
            full_name=user["full_name"],
            email=user["email"],
            role_id=user["role_id"],
        )
        return LoginResponse(
            success=True,
            message="Login exitoso",
            user=authenticated_user,
        )
