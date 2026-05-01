"""Reglas de negocio del módulo de usuarios."""

from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserSummary


class UserService:
    """Coordina casos de uso relacionados con usuarios."""

    def __init__(self) -> None:
        self.repository = UserRepository()

    def list_users(self) -> list[UserSummary]:
        """Retorna una lista vacía hasta conectar persistencia real."""
        return self.repository.list_users()

