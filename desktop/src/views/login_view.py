"""Vista inicial de login.

El inicio de sesión usará RUT chileno y contraseña. Esta vista usa PySide6 como
base recomendada, pero puede adaptarse a Tkinter conservando la separación entre
vista, controlador y servicios.
"""

from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget


class LoginView(QWidget):
    """Ventana base para el ingreso de usuarios en la interfaz desktop."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("VecinoSeguro - Login")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("VecinoSeguro"))
        layout.addWidget(QLabel("Ingreso con RUT y contraseña"))
        layout.addWidget(QLineEdit(placeholderText="RUT"))
        password_input = QLineEdit(placeholderText="Contraseña")
        password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(password_input)
        layout.addWidget(QPushButton("Ingresar"))

        self.setLayout(layout)
