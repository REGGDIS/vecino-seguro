"""Helpers de UI compartidos entre vistas.

Aplicar estilos a `QPushButton` mediante `setStyleSheet` directo al widget
evita un problema conocido en Qt: cuando un selector de QSS global tiene
`background-color`, los QPushButton hijos pueden no rellenar correctamente
su fondo dependiendo del tema nativo de la plataforma.

Usar estos helpers garantiza un render visual consistente en Windows,
Linux y macOS.
"""

from PySide6.QtWidgets import QPushButton


_BUTTON_STYLES = {
    "primary": """
        QPushButton {
            background-color: #1B4F8C;
            color: #FFFFFF;
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-size: 13px;
            font-weight: 600;
        }
        QPushButton:hover    { background-color: #0F3866; }
        QPushButton:pressed  { background-color: #0A2647; }
        QPushButton:disabled { background-color: #9CA3AF; }
    """,
    "success": """
        QPushButton {
            background-color: #34A853;
            color: #FFFFFF;
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-size: 13px;
            font-weight: 600;
        }
        QPushButton:hover   { background-color: #2C8C46; }
        QPushButton:pressed { background-color: #25733A; }
    """,
    "secondary": """
        QPushButton {
            background-color: #FFFFFF;
            color: #1B4F8C;
            border: 1.5px solid #1B4F8C;
            border-radius: 6px;
            padding: 9px 20px;
            font-size: 13px;
            font-weight: 600;
        }
        QPushButton:hover { background-color: #EEF3FA; }
    """,
    "danger": """
        QPushButton {
            background-color: #E53E3E;
            color: #FFFFFF;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 12px;
            font-weight: 600;
        }
        QPushButton:hover { background-color: #C53030; }
    """,
}


def estilizar_boton(boton: QPushButton, variante: str) -> QPushButton:
    """Aplica un estilo predefinido a un QPushButton existente."""
    if variante in _BUTTON_STYLES:
        boton.setStyleSheet(_BUTTON_STYLES[variante])
    return boton
