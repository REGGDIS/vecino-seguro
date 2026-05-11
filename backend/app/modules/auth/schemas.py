"""Modelos Pydantic para autenticación."""

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Datos requeridos para iniciar sesión."""

    rut: str = Field(..., examples=["11111111-1"])
    password: str = Field(..., min_length=1, examples=["admin1234"])


class AuthenticatedUser(BaseModel):
    """Datos seguros del usuario autenticado."""

    id: int
    rut: str
    full_name: str
    email: str
    role_id: int


class LoginResponse(BaseModel):
    """Respuesta segura del flujo de login."""

    success: bool
    message: str
    user: AuthenticatedUser
