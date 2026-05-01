"""Modelos Pydantic para autenticación."""

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Datos requeridos para iniciar sesión."""

    rut: str = Field(..., examples=["12.345.678-5"])
    password: str = Field(..., min_length=8, examples=["change_me_secure"])


class LoginResponse(BaseModel):
    """Respuesta inicial del flujo de login."""

    message: str
    token: str | None = None

