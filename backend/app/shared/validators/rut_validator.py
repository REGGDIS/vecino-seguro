"""Validador de RUT chileno mediante algoritmo módulo 11."""

import re


def clean_rut(rut: str) -> str:
    """Elimina puntos, guion y espacios para normalizar el RUT."""
    return re.sub(r"[^0-9kK]", "", rut or "").upper()


def validate_rut(rut: str) -> bool:
    """Valida un RUT chileno usando el dígito verificador módulo 11.

    Esta función será usada inicialmente en el flujo de login antes de consultar
    credenciales reales en la base de datos.
    """
    cleaned = clean_rut(rut)
    if len(cleaned) < 2 or not cleaned[:-1].isdigit():
        return False

    body = cleaned[:-1]
    verifier = cleaned[-1]
    multiplier = 2
    total = 0

    for digit in reversed(body):
        total += int(digit) * multiplier
        multiplier = 2 if multiplier == 7 else multiplier + 1

    remainder = 11 - (total % 11)
    expected = "0" if remainder == 11 else "K" if remainder == 10 else str(remainder)

    return verifier == expected

