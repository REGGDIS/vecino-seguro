"""Vista base del panel principal.

Esta pantalla mostrará en el futuro un resumen de emergencias, estados recientes
y acciones disponibles para vecinos o administradores. La implementación visual
puede mantenerse en PySide6 o adaptarse a Tkinter sin cambiar controladores.
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
