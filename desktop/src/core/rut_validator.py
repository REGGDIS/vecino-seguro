"""Validador de RUT chileno mediante algoritmo Módulo 11.

Forma parte del núcleo (`core`) porque la validación de RUT es una regla
transversal que utilizan tanto las vistas (validación en vivo) como los
controladores (validación previa al envío al backend).
"""

import re


class RutValidator:
    """Valida y formatea RUT chileno."""

    @staticmethod
    def limpiar(rut: str) -> str:
        if not rut:
            return ""
        return re.sub(r"[.\-\s]", "", rut).upper()

    @staticmethod
    def calcular_dv(cuerpo: str) -> str:
        """Calcula el dígito verificador esperado para un cuerpo numérico.

        Algoritmo Módulo 11:
          1. Multiplicar cada dígito (de derecha a izquierda) por la serie
             2,3,4,5,6,7 que se reinicia al llegar a 7.
          2. Sumar los productos.
          3. resto = 11 - (suma mod 11)
          4. resto = 11 -> '0', resto = 10 -> 'K', otro -> str(resto)
        """
        if not cuerpo.isdigit():
            return ""

        suma = 0
        multiplicador = 2
        for digito in reversed(cuerpo):
            suma += int(digito) * multiplicador
            multiplicador = 2 if multiplicador == 7 else multiplicador + 1

        resto = 11 - (suma % 11)
        if resto == 11:
            return "0"
        if resto == 10:
            return "K"
        return str(resto)

    @classmethod
    def es_valido(cls, rut: str) -> bool:
        rut_limpio = cls.limpiar(rut)
        if len(rut_limpio) < 2:
            return False
        cuerpo, dv_ingresado = rut_limpio[:-1], rut_limpio[-1]
        if not cuerpo.isdigit():
            return False
        if not (1_000_000 <= int(cuerpo) <= 99_999_999):
            return False
        return cls.calcular_dv(cuerpo) == dv_ingresado

    @classmethod
    def formatear(cls, rut: str) -> str:
        """Formatea como 12.345.678-9."""
        rut_limpio = cls.limpiar(rut)
        if len(rut_limpio) < 2:
            return rut
        cuerpo, dv = rut_limpio[:-1], rut_limpio[-1]
        cuerpo_formateado = ""
        for i, digito in enumerate(reversed(cuerpo)):
            if i > 0 and i % 3 == 0:
                cuerpo_formateado = "." + cuerpo_formateado
            cuerpo_formateado = digito + cuerpo_formateado
        return f"{cuerpo_formateado}-{dv}"
