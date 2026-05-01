"""Punto de entrada de la interfaz desktop en Python de VecinoSeguro.

La implementación base usa PySide6 como opción recomendada. Si el equipo migra
a Tkinter, este archivo puede adaptarse manteniendo el rol de punto de entrada.
"""

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

# Permite ejecutar `python src/main/main.py` desde la carpeta desktop.
sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.views.login_view import LoginView


def main() -> int:
    """Inicia la aplicación desktop con una ventana mínima de login."""
    app = QApplication(sys.argv)
    window = LoginView()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
