"""Servicio de contraseñas: hashing, verificación y validación de criterios.

Para el prototipo se utiliza la biblioteca estándar (`hashlib` + `secrets`)
para no introducir dependencias adicionales. Cuando el backend FastAPI
asuma la autenticación, esta utilidad seguirá siendo útil para validar
criterios localmente antes de enviar la solicitud.
"""

import hashlib
import re
import secrets


class PasswordService:
    """Hashea, verifica y valida contraseñas."""

    LARGO_MINIMO = 8

    @classmethod
    def validar_criterios(cls, password: str) -> tuple[bool, str]:
        if len(password) < cls.LARGO_MINIMO:
            return False, f"Debe tener al menos {cls.LARGO_MINIMO} caracteres."
        if not re.search(r"[A-Z]", password):
            return False, "Debe contener al menos una mayúscula."
        if not re.search(r"[a-z]", password):
            return False, "Debe contener al menos una minúscula."
        if not re.search(r"\d", password):
            return False, "Debe contener al menos un número."
        return True, ""

    @staticmethod
    def hash_password(password: str) -> str:
        """Genera hash SHA-256 con sal aleatoria. Formato: 'salt$hash'."""
        salt = secrets.token_hex(16)
        digest = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
        return f"{salt}${digest}"

    @staticmethod
    def verificar(password: str, password_hash: str) -> bool:
        try:
            salt, digest_esperado = password_hash.split("$", 1)
        except ValueError:
            return False
        digest_calculado = hashlib.sha256(
            (salt + password).encode("utf-8")
        ).hexdigest()
        return secrets.compare_digest(digest_calculado, digest_esperado)
