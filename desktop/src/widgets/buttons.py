"""Botones estilizados de VecinoSeguro.

Los botones se aplican mediante `setStyleSheet` directo al widget para
evitar conflictos del QSS global con QPushButton (problema conocido en
Qt cuando el selector universal define `background-color`).

Variantes disponibles:
    primary    Azul. Acciones principales.
    success    Verde. Confirmaciones.
    secondary  Borde azul. Acciones importantes pero no principales.
    outline    Borde suave. Cancelar, volver, cerrar.
    danger     Rojo. Acciones críticas o destructivas.
    disabled   Solo placeholder visual; usar `setEnabled(False)`.
"""

from PySide6.QtWidgets import QPushButton

from src.core.colors import Colors


_BUTTON_STYLES = {
    "primary": f"""
        QPushButton {{
            background-color: {Colors.PRIMARY};
            color: {Colors.WHITE};
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-size: 13px;
            font-weight: 600;
        }}
        QPushButton:hover    {{ background-color: {Colors.DARK_PRIMARY}; }}
        QPushButton:pressed  {{ background-color: #042748; }}
        QPushButton:disabled {{ background-color: #B0BFCC; }}
    """,
    "success": f"""
        QPushButton {{
            background-color: {Colors.SUCCESS};
            color: {Colors.WHITE};
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-size: 13px;
            font-weight: 600;
        }}
        QPushButton:hover   {{ background-color: {Colors.DARK_SUCCESS}; }}
        QPushButton:pressed {{ background-color: #0F6320; }}
    """,
    "secondary": f"""
        QPushButton {{
            background-color: {Colors.WHITE};
            color: {Colors.PRIMARY};
            border: 1.5px solid {Colors.PRIMARY};
            border-radius: 6px;
            padding: 9px 20px;
            font-size: 13px;
            font-weight: 600;
        }}
        QPushButton:hover {{ background-color: #E5F0FB; }}
    """,
    "outline": f"""
        QPushButton {{
            background-color: {Colors.WHITE};
            color: {Colors.TEXT_SECONDARY};
            border: 1.5px solid {Colors.BORDER};
            border-radius: 6px;
            padding: 9px 20px;
            font-size: 13px;
            font-weight: 600;
        }}
        QPushButton:hover {{ background-color: {Colors.SURFACE}; }}
    """,
    "danger": f"""
        QPushButton {{
            background-color: {Colors.DANGER};
            color: {Colors.WHITE};
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 12px;
            font-weight: 600;
        }}
        QPushButton:hover {{ background-color: #B11D14; }}
    """,
}


def estilizar_boton(boton: QPushButton, variante: str) -> QPushButton:
    """Aplica un estilo predefinido a un QPushButton existente.

    Args:
        boton: QPushButton al que se aplicará el estilo.
        variante: Una de "primary", "success", "secondary", "outline", "danger".

    Returns:
        El mismo botón, para permitir encadenamiento.
    """
    if variante in _BUTTON_STYLES:
        boton.setStyleSheet(_BUTTON_STYLES[variante])
    return boton


def crear_boton(texto: str, variante: str = "primary",
                alto_min: int = 40) -> QPushButton:
    """Crea un QPushButton estilizado en una sola llamada."""
    boton = QPushButton(texto)
    estilizar_boton(boton, variante)
    boton.setMinimumHeight(alto_min)
    return boton
