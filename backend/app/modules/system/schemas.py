"""Modelos Pydantic para información del sistema."""

from pydantic import BaseModel


class SystemInfo(BaseModel):
    """Información general del backend VecinoSeguro."""

    app_name: str
    version: str
    environment: str
    status: str
    message: str