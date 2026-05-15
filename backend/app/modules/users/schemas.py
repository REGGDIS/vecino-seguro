"""Modelos Pydantic del módulo de usuarios."""

from pydantic import BaseModel, Field


class UserSummary(BaseModel):
    """Resumen público de usuario para listados futuros."""

    id: int
    rut: str
    full_name: str
    role: str


class UserCreateRequest(BaseModel):
    """Datos requeridos para registrar un usuario real."""

    rut: str = Field(...)
    full_name: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    role_id: int


class UserCreateResponse(BaseModel):
    """Respuesta segura para altas de usuario, sin contraseña ni hash."""

    id: int
    rut: str
    full_name: str
    email: str
    role_id: int
