"""Rutas base para gestión de usuarios."""

from fastapi import APIRouter, HTTPException, status

from app.modules.users.schemas import (
    UserActiveUpdateRequest,
    UserCreateRequest,
    UserCreateResponse,
    UserListItem,
    UserUpdateRequest,
)
from app.modules.users.service import (
    InvalidRoleError,
    InvalidUserDataError,
    UserAlreadyExistsError,
    UserActivationError,
    UserNotFoundError,
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
    except (InvalidUserDataError, InvalidRoleError, UserActivationError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except UserAlreadyExistsError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="No fue posible crear el usuario",
        ) from exc


@router.patch("/{user_id}", response_model=UserListItem)
def update_user(user_id: int, user_data: UserUpdateRequest) -> UserListItem:
    """Actualiza nombre, email y rol de un usuario existente."""
    try:
        return user_service.update_user(user_id, user_data)
    except (InvalidUserDataError, InvalidRoleError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except UserNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except UserAlreadyExistsError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="No fue posible actualizar el usuario",
        ) from exc


@router.patch("/{user_id}/active", response_model=UserListItem)
def update_user_active_status(
    user_id: int,
    user_data: UserActiveUpdateRequest,
) -> UserListItem:
    """Activa o desactiva un usuario sin eliminarlo."""
    try:
        return user_service.update_active_status(user_id, user_data)
    except (InvalidUserDataError, UserActivationError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except UserNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="No fue posible cambiar el estado del usuario",
        ) from exc
