"""Reglas de negocio del módulo de usuarios."""

from mysql.connector import IntegrityError
from passlib.context import CryptContext

from app.modules.users.repository import UserRepository
from app.modules.users.schemas import (
    UserCreateRequest,
    UserCreateResponse,
    UserSummary,
)
from app.shared.validators.rut_validator import normalize_rut, validate_rut


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
VALID_ROLE_IDS = {1, 2}


class InvalidUserDataError(ValueError):
    """Indica que los datos enviados no cumplen reglas mínimas."""


class UserAlreadyExistsError(ValueError):
    """Indica que RUT o email ya pertenecen a otro usuario."""


class InvalidRoleError(ValueError):
    """Indica que el rol solicitado no está permitido."""


class UserService:
    """Coordina casos de uso relacionados con usuarios."""

    def __init__(self) -> None:
        self.repository = UserRepository()

    def list_users(self) -> list[UserSummary]:
        """Retorna una lista vacía hasta conectar persistencia real."""
        return self.repository.list_users()

    def create_user(self, request: UserCreateRequest) -> UserCreateResponse:
        """Valida, hashea contraseña y registra un usuario real."""
        rut = request.rut.strip()
        full_name = request.full_name.strip()
        email = request.email.strip().lower()
        password = request.password.strip()
        role_id = request.role_id

        if not validate_rut(rut):
            raise InvalidUserDataError("RUT inválido")
        normalized_rut = normalize_rut(rut)

        if not full_name:
            raise InvalidUserDataError("El nombre completo es obligatorio")
        if not email:
            raise InvalidUserDataError("El email es obligatorio")
        if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
            raise InvalidUserDataError("El email no tiene un formato válido")
        if not password or len(password) < 6:
            raise InvalidUserDataError(
                "La contraseña inicial debe tener al menos 6 caracteres"
            )
        if role_id not in VALID_ROLE_IDS:
            raise InvalidRoleError("Rol inválido. Use 1 para admin o 2 para vecino")
        if not self.repository.role_exists(role_id):
            raise InvalidRoleError("El rol indicado no existe")

        if self.repository.find_by_rut(normalized_rut) is not None:
            raise UserAlreadyExistsError("Ya existe un usuario con ese RUT")
        if self.repository.find_by_email(email) is not None:
            raise UserAlreadyExistsError("Ya existe un usuario con ese email")

        password_hash = pwd_context.hash(password)
        try:
            return self.repository.create_user(
                rut=normalized_rut,
                full_name=full_name,
                email=email,
                password_hash=password_hash,
                role_id=role_id,
            )
        except IntegrityError as exc:
            if getattr(exc, "errno", None) == 1062:
                raise UserAlreadyExistsError(
                    "Ya existe un usuario con ese RUT o email"
                ) from exc
            raise
