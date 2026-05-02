"""Vista base del panel principal.

Esta pantalla mostrará en el futuro un resumen de emergencias, estados recientes
y acciones disponibles para vecinos o administradores usando componentes PySide6.
"""

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class DashboardView(QWidget):
    """Panel principal de la interfaz desktop."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("VecinoSeguro - Panel")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Resumen de emergencias pendiente de implementar"))
        self.setLayout(layout)
