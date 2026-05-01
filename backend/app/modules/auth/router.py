"""Rutas base para autenticación.

El login considera RUT y contraseña, pero todavía no consulta una base de datos
real ni emite tokens definitivos.
"""

from fastapi import APIRouter, HTTPException, status

from app.modules.auth.schemas import LoginRequest, LoginResponse
from app.modules.auth.service import AuthService

router = APIRouter()
auth_service = AuthService()


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    """Valida formato inicial de credenciales y deja preparado el login real."""
    result = auth_service.validate_login_request(payload.rut, payload.password)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="RUT o contraseña con formato inválido.",
        )

    return LoginResponse(
        message="Solicitud de login válida. Integración con base de datos pendiente.",
        token=None,
    )

