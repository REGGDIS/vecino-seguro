"""Modelos Pydantic del módulo de usuarios."""

from pydantic import BaseModel


class UserSummary(BaseModel):
    """Resumen público de usuario para listados futuros."""

    id: int
    rut: str
    full_name: str
    role: str

