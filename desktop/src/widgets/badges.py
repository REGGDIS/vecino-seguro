"""Etiquetas de estado (badges) con estilos coherentes.

Permite presentar de forma uniforme los estados de los reportes y los
niveles de urgencia tanto en tablas, listados como en paneles de detalle.
Los colores se obtienen de la guía oficial de identidad corporativa.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from src.core.colors import Colors


_ESTADO_STYLES = {
    "Pendiente":   (Colors.BG_WARNING, Colors.WARNING),
    "En revisión": (Colors.BG_INFO,    Colors.INFO),
    "Atendido":    (Colors.BG_SUCCESS, Colors.SUCCESS),
    "Resuelto":    (Colors.BG_NEUTRAL, Colors.TEXT_SECONDARY),
}

_URGENCIA_STYLES = {
    "Crítica": ("#FED7D7", Colors.DANGER),
    "Alta":    ("#FEEBC8", "#C05621"),
    "Media":   ("#FEFCBF", "#975A16"),
    "Baja":    ("#C6F6D5", Colors.DARK_SUCCESS),
}


def _aplicar_badge_style(label: QLabel, bg: str, fg: str,
                         peso: int = 600) -> None:
    """Aplica el estilo de píldora a un QLabel existente."""
    label.setStyleSheet(
        f"background-color: {bg}; color: {fg}; "
        f"border: none; border-radius: 10px; "
        f"padding: 4px 12px; font-weight: {peso}; font-size: 11px;"
    )
    label.setAlignment(Qt.AlignCenter)


def estilizar_badge_estado(label: QLabel, estado: str) -> QLabel:
    """Aplica al label el estilo correspondiente al estado del reporte."""
    bg, fg = _ESTADO_STYLES.get(estado, (Colors.BG_NEUTRAL, Colors.TEXT_SECONDARY))
    label.setText(estado)
    _aplicar_badge_style(label, bg, fg, peso=600)
    return label


def estilizar_badge_urgencia(label: QLabel, urgencia: str,
                             con_punto: bool = True) -> QLabel:
    """Aplica al label el estilo correspondiente al nivel de urgencia."""
    bg, fg = _URGENCIA_STYLES.get(urgencia, (Colors.BG_NEUTRAL, Colors.TEXT_SECONDARY))
    texto = f"● {urgencia}" if con_punto else urgencia
    label.setText(texto)
    _aplicar_badge_style(label, bg, fg, peso=700)
    return label


def crear_badge_estado(estado: str) -> QLabel:
    """Crea un nuevo QLabel ya estilizado como badge de estado."""
    return estilizar_badge_estado(QLabel(""), estado)


def crear_badge_urgencia(urgencia: str, con_punto: bool = True) -> QLabel:
    """Crea un nuevo QLabel ya estilizado como badge de urgencia."""
    return estilizar_badge_urgencia(QLabel(""), urgencia, con_punto)
