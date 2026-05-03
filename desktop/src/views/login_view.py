"""Vista de login con validación de RUT y contraseña.

Usa PySide6 como base recomendada por la guía del proyecto. Toda la lógica
de validación se delega al `AuthController`, lo que mantiene la vista
desacoplada del modelo de datos y permite migrar a Tkinter sin reescribir
la lógica de negocio.
"""

from pathlib import Path

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.controllers.auth_controller import AuthController
from src.core.rut_validator import RutValidator
from src.widgets.buttons import estilizar_boton

LOGO_PATH = str(Path(__file__).resolve().parents[1] / "assets" / "logo.svg")


class LoginView(QWidget):
    """Pantalla de inicio de sesión."""

    login_exitoso = Signal(object)  # emite el Usuario autenticado

    def __init__(self, auth_controller: AuthController | None = None) -> None:
        super().__init__()
        self._auth = auth_controller or AuthController()
        self.setWindowTitle("VecinoSeguro · Iniciar sesión")
        self.resize(960, 620)
        self._build_ui()

    def _build_ui(self) -> None:
        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ===== Panel izquierdo (branding) =====
        izquierda = QFrame()
        izquierda.setStyleSheet("background-color: #073B6B;")
        izq_layout = QVBoxLayout(izquierda)
        izq_layout.setContentsMargins(60, 60, 60, 60)
        izq_layout.setSpacing(20)
        izq_layout.addStretch()

        logo = QSvgWidget(LOGO_PATH)
        logo.setFixedSize(QSize(140, 140))
        logo.setStyleSheet("background: transparent;")
        izq_layout.addWidget(logo, alignment=Qt.AlignCenter)

        marca = QLabel("VecinoSeguro")
        marca.setStyleSheet(
            "color: #FFFFFF; font-size: 36px; font-weight: 800; letter-spacing: 0.5px;"
        )
        marca.setAlignment(Qt.AlignCenter)
        izq_layout.addWidget(marca)

        eslogan = QLabel("Comunidad conectada,\nrespuesta inmediata.")
        eslogan.setStyleSheet("color: #C8D4E5; font-size: 16px;")
        eslogan.setAlignment(Qt.AlignCenter)
        izq_layout.addWidget(eslogan)
        izq_layout.addStretch()

        pie = QLabel("Taller de Ingeniería de Software · 2026")
        pie.setStyleSheet("color: #6B85A8; font-size: 11px;")
        pie.setAlignment(Qt.AlignCenter)
        izq_layout.addWidget(pie)

        # ===== Panel derecho (formulario) =====
        derecha = QFrame()
        derecha.setStyleSheet("background-color: #FFFFFF;")
        der_layout = QVBoxLayout(derecha)
        der_layout.setContentsMargins(80, 60, 80, 60)
        der_layout.setSpacing(0)
        der_layout.addStretch()

        titulo = QLabel("Iniciar sesión")
        titulo.setStyleSheet("color: #073B6B; font-size: 28px; font-weight: 700;")
        der_layout.addWidget(titulo)

        subtitulo = QLabel("Ingresa con tu RUT y contraseña")
        subtitulo.setStyleSheet("color: #52616B; font-size: 14px;")
        der_layout.addWidget(subtitulo)
        der_layout.addSpacing(32)

        der_layout.addWidget(self._mk_field_label("RUT"))
        der_layout.addSpacing(6)
        self.input_rut = QLineEdit()
        self.input_rut.setPlaceholderText("12.345.678-5")
        self.input_rut.editingFinished.connect(self._formatear_rut)
        self.input_rut.textChanged.connect(self._on_rut_changed)
        der_layout.addWidget(self.input_rut)

        self.lbl_rut_status = QLabel("")
        self.lbl_rut_status.setStyleSheet("font-size: 11px; min-height: 14px;")
        der_layout.addWidget(self.lbl_rut_status)
        der_layout.addSpacing(8)

        der_layout.addWidget(self._mk_field_label("Contraseña"))
        der_layout.addSpacing(6)
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setPlaceholderText("••••••••")
        self.input_password.returnPressed.connect(self._intentar_login)
        der_layout.addWidget(self.input_password)
        der_layout.addSpacing(20)

        self.lbl_error = QLabel("")
        self.lbl_error.setObjectName("errorMsg")
        self.lbl_error.setVisible(False)
        self.lbl_error.setWordWrap(True)
        der_layout.addWidget(self.lbl_error)
        der_layout.addSpacing(8)

        btn = QPushButton("Ingresar")
        estilizar_boton(btn, "primary")
        btn.setMinimumHeight(44)
        btn.clicked.connect(self._intentar_login)
        der_layout.addWidget(btn)
        der_layout.addSpacing(24)

        # Cuentas demo
        demo_card = QFrame()
        demo_card.setStyleSheet(
            "background-color: #F4F8FB; border: 1px dashed #D9E2EC; border-radius: 8px;"
        )
        demo_layout = QVBoxLayout(demo_card)
        demo_layout.setSpacing(4)
        demo_layout.setContentsMargins(14, 12, 14, 12)
        demo_layout.addWidget(self._mk_demo_titulo("Cuentas de prueba"))
        demo_layout.addWidget(self._mk_demo_linea("Vecino:", "12.345.678-5", "Vecino123"))
        demo_layout.addWidget(self._mk_demo_linea("Admin:", "11.111.111-1", "Admin123"))
        der_layout.addWidget(demo_card)

        der_layout.addStretch()

        outer.addWidget(izquierda, 4)
        outer.addWidget(derecha, 5)

    # ---- helpers de creación de etiquetas ----
    def _mk_field_label(self, texto: str) -> QLabel:
        l = QLabel(texto)
        l.setStyleSheet("color: #52616B; font-weight: 600; font-size: 12px;")
        return l

    def _mk_demo_titulo(self, texto: str) -> QLabel:
        l = QLabel(texto)
        l.setStyleSheet(
            "color: #52616B; font-weight: 700; font-size: 11px; "
            "text-transform: uppercase; letter-spacing: 0.8px; background: transparent;"
        )
        return l

    def _mk_demo_linea(self, rol: str, rut: str, password: str) -> QLabel:
        l = QLabel(
            f"<span style='color:#005A9C; font-weight:600;'>{rol}</span> "
            f"<span style='color:#102A43;'>{rut}</span> "
            f"<span style='color:#52616B;'>·</span> "
            f"<span style='color:#102A43;'>{password}</span>"
        )
        l.setStyleSheet("font-size: 12px; background: transparent;")
        return l

    # ---- eventos ----
    def _formatear_rut(self) -> None:
        texto = self.input_rut.text().strip()
        if texto:
            self.input_rut.setText(RutValidator.formatear(texto))

    def _on_rut_changed(self, texto: str) -> None:
        self.lbl_error.setVisible(False)
        if not texto.strip():
            self.lbl_rut_status.setText("")
            return
        if RutValidator.es_valido(texto):
            self.lbl_rut_status.setStyleSheet("color: #16812C; font-size: 11px;")
            self.lbl_rut_status.setText("✓ RUT válido")
        else:
            self.lbl_rut_status.setStyleSheet("color: #9CA3AF; font-size: 11px;")
            self.lbl_rut_status.setText("Verificando dígito verificador…")

    def _intentar_login(self) -> None:
        rut = self.input_rut.text().strip()
        password = self.input_password.text()
        resultado = self._auth.login_detallado(rut, password)
        if resultado.exito:
            self.lbl_error.setVisible(False)
            self.input_password.clear()
            self.login_exitoso.emit(resultado.usuario)
        else:
            self.lbl_error.setText(resultado.mensaje)
            self.lbl_error.setVisible(True)
