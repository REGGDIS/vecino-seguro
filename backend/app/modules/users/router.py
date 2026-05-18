"""Rutas base para gestión de usuarios."""

from fastapi import APIRouter, HTTPException, status

from app.modules.users.schemas import (
    UserCreateRequest,
    UserCreateResponse,
    UserListItem,
)
from app.modules.users.service import (
    InvalidRoleError,
    InvalidUserDataError,
    UserAlreadyExistsError,
    UserService,
)

router = APIRouter()
user_service = UserService()


@router.get("/", response_model=list[UserListItem])
def list_users() -> list[UserListItem]:
    """Lista usuarios reales sin exponer contraseña ni hash."""
    try:
        return user_service.list_users()
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="No fue posible obtener los usuarios",
        ) from exc


@router.post(
    "/",
    response_model=UserCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(user_data: UserCreateRequest) -> UserCreateResponse:
    """Crea un usuario real en MySQL/MariaDB sin exponer contraseña."""
    try:
        return user_service.create_user(user_data)
    except (InvalidUserDataError, InvalidRoleError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except UserAlreadyExistsError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="No fue posible crear el usuario",
        ) from exc
