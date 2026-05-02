"""Punto de entrada de la aplicación desktop de VecinoSeguro.

Este módulo actúa como contenedor de dependencias del prototipo:
construye una sola vez los repositorios y los inyecta en los controladores,
los controladores se inyectan en las vistas. Esto refleja el Principio de
Inversión de Dependencias (DIP) de SOLID.

Si el equipo decide migrar la interfaz a Tkinter, este archivo cambiará
para crear las vistas Tkinter, pero los controladores y repositorios se
mantendrán intactos.
"""

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

# Permite ejecutar `python src/main/main.py` desde la carpeta desktop.
sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.config.settings import settings
from src.controllers.auth_controller import AuthController
from src.controllers.emergency_controller import EmergencyController
from src.repositories.emergency_repository import EmergencyRepository
from src.repositories.user_repository import UserRepository
from src.views.login_view import LoginView
from src.views.main_window import MainWindow

ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"
QSS_PATH = ASSETS_DIR / "app.qss"


def cargar_estilos() -> str:
    if QSS_PATH.exists():
        return QSS_PATH.read_text(encoding="utf-8")
    return ""


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName(settings.app_name)
    # Forzar estilo Fusion para garantizar render consistente del QSS
    # (el estilo nativo de cada plataforma a veces ignora background-color).
    app.setStyle("Fusion")
    app.setStyleSheet(cargar_estilos())

    # ---- Contenedor de dependencias ----
    user_repo = UserRepository()
    emergency_repo = EmergencyRepository()
    auth_controller = AuthController(user_repository=user_repo)
    emergency_controller = EmergencyController(repository=emergency_repo)

    # ---- Orquestación de ventanas ----
    state: dict = {"main": None, "login": None}

    def mostrar_main(usuario):
        win = MainWindow(
            auth_controller=auth_controller,
            emergency_controller=emergency_controller,
            on_logout=mostrar_login,
        )
        win.set_usuario(usuario)
        win.show()
        state["main"] = win
        if state["login"] is not None:
            state["login"].close()
            state["login"] = None

    def mostrar_login():
        win = LoginView(auth_controller)
        win.login_exitoso.connect(mostrar_main)
        win.show()
        state["login"] = win
        if state["main"] is not None:
            state["main"].close()
            state["main"] = None

    mostrar_login()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
