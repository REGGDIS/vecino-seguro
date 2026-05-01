"""Servicio de autenticación.

Aquí se concentrará la lógica de validación, comparación de hash de contraseña
y emisión de tokens cuando el prototipo avance.
"""

from app.shared.validators.rut_validator import validate_rut


class AuthService:
    """Servicio responsable de reglas de negocio del módulo de autenticación."""

    def validate_login_request(self, rut: str, password: str) -> bool:
        """Valida datos mínimos antes de intentar autenticar contra la base."""
        return validate_rut(rut) and len(password.strip()) >= 8

