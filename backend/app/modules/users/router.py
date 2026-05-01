"""Rutas base para gestión de usuarios."""

from fastapi import APIRouter

from app.modules.users.schemas import UserSummary
from app.modules.users.service import UserService

router = APIRouter()
user_service = UserService()


@router.get("/", response_model=list[UserSummary])
def list_users() -> list[UserSummary]:
    """Ruta placeholder para listar usuarios en futuras iteraciones."""
    return user_service.list_users()

