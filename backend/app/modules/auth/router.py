"""Rutas base para autenticación."""

from fastapi import APIRouter, HTTPException, status

from app.modules.auth.schemas import LoginRequest, LoginResponse
from app.modules.auth.service import (
    AuthService,
    InvalidCredentialsError,
    InvalidLoginDataError,
)

router = APIRouter()
auth_service = AuthService()


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    """Autentica un usuario con RUT y contraseña."""
    try:
        return auth_service.login(payload.rut, payload.password)
    except InvalidLoginDataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="RUT o contraseña con formato inválido.",
        ) from None
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="RUT o contraseña incorrectos",
        ) from None
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al procesar login.",
        ) from None
