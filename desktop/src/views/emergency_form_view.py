"""Vista base para registrar emergencias.

Campos futuros sugeridos: tipo, descripción, ubicación y nivel de urgencia.
La estructura actual usa PySide6 y mantiene la responsabilidad visual separada
de controladores y servicios.
"""

from PySide6.QtWidgets import QLabel, QLineEdit, QTextEdit, QVBoxLayout, QWidget


class EmergencyFormView(QWidget):
    """Formulario inicial para crear reportes de emergencia en desktop."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("VecinoSeguro - Registrar emergencia")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Registrar emergencia"))
        layout.addWidget(QLineEdit(placeholderText="Tipo de emergencia"))
        layout.addWidget(QTextEdit(placeholderText="Descripción"))
        layout.addWidget(QLineEdit(placeholderText="Ubicación"))
        layout.addWidget(QLineEdit(placeholderText="Nivel de urgencia"))
        self.setLayout(layout)
