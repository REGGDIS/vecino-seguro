"""Punto de entrada de la interfaz desktop PySide6 de VecinoSeguro."""

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
