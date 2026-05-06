"""Ventana principal: shell con sidebar y conmutación de páginas.

Contiene la navegación lateral, una barra superior, y un `QStackedWidget`
con las tres vistas principales: dashboard, formulario de registro y
listado de reportes. Coordina la sesión a través del `AuthController`.
"""

from pathlib import Path

from PySide6.QtCore import QSize, Qt
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from src.controllers.auth_controller import AuthController
from src.controllers.emergency_controller import EmergencyController
from src.core.constants import (
    APP_DISPLAY_NAME,
    DEFAULT_WINDOW_HEIGHT,
    DEFAULT_WINDOW_WIDTH,
)
from src.models.entities import Rol, Usuario
from src.views.dashboard_view import DashboardView
from src.views.emergency_form_view import EmergencyFormView
from src.views.emergency_list_view import EmergencyListView

LOGO_PATH = str(Path(__file__).resolve().parents[1] / "assets" / "logo.svg")


class MainWindow(QMainWindow):
    """Ventana principal posterior al login."""

    PAG_DASH, PAG_FORM, PAG_LIST = 0, 1, 2

    def __init__(
        self,
        auth_controller: AuthController,
        emergency_controller: EmergencyController,
        on_logout,
    ) -> None:
        super().__init__()
        self._auth = auth_controller
        self._emergency = emergency_controller
        self._on_logout = on_logout
        self._usuario: Usuario | None = None

        self.setWindowTitle(APP_DISPLAY_NAME)
        self.resize(max(DEFAULT_WINDOW_WIDTH, 1240),
                    max(DEFAULT_WINDOW_HEIGHT, 780))
        self.setMinimumSize(1080, 680)
        self._build_ui()

    def _build_ui(self) -> None:
        central = QWidget()
        central.setObjectName("central")
        central.setStyleSheet("QWidget#central { background-color: #F4F8FB; }")
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ===== Sidebar =====
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(240)
        sb = QVBoxLayout(self.sidebar)
        sb.setContentsMargins(0, 24, 0, 24)
        sb.setSpacing(0)

        # Brand
        brand_box = QHBoxLayout()
        brand_box.setContentsMargins(20, 0, 20, 0)
        brand_box.setSpacing(10)
        logo = QSvgWidget(LOGO_PATH)
        logo.setFixedSize(QSize(34, 34))
        logo.setStyleSheet("background: transparent;")
        brand_box.addWidget(logo)

        brand_inner = QHBoxLayout()
        brand_inner.setContentsMargins(0, 0, 0, 0)
        brand_inner.setSpacing(0)
        lbl_brand_a = QLabel("Vecino")
        lbl_brand_a.setStyleSheet(
            "color: #FFFFFF; font-size: 18px; font-weight: 800; "
            "background: transparent; border: none;"
        )
        lbl_brand_b = QLabel("Seguro")
        lbl_brand_b.setStyleSheet(
            "color: #22A63A; font-size: 18px; font-weight: 800; "
            "background: transparent; border: none;"
        )
        brand_inner.addWidget(lbl_brand_a)
        brand_inner.addWidget(lbl_brand_b)
        brand_box.addLayout(brand_inner)
        brand_box.addStretch()
        sb.addLayout(brand_box)
        sb.addSpacing(28)

        sb.addWidget(self._mk_sidebar_section("PRINCIPAL"))
        self.btn_dash = self._mk_sidebar_btn("🏠  Inicio",
                                             lambda: self.ir_a(self.PAG_DASH))
        self.btn_form = self._mk_sidebar_btn("➕  Reportar",
                                             lambda: self.ir_a(self.PAG_FORM))
        self.btn_list = self._mk_sidebar_btn("📋  Reportes",
                                             lambda: self.ir_a(self.PAG_LIST))
        for b in (self.btn_dash, self.btn_form, self.btn_list):
            sb.addWidget(b)
        sb.addSpacing(20)

        sb.addWidget(self._mk_sidebar_section("CUENTA"))
        user_wrapper = QHBoxLayout()
        user_wrapper.setContentsMargins(16, 4, 16, 4)
        self.user_card = QFrame()
        self.user_card.setObjectName("userCard")
        uc = QVBoxLayout(self.user_card)
        uc.setContentsMargins(14, 12, 14, 12)
        uc.setSpacing(2)
        self.lbl_user_nombre = QLabel("—")
        self.lbl_user_nombre.setStyleSheet(
            "color: #FFFFFF; font-weight: 700; font-size: 13px; "
            "background: transparent; border: none;"
        )
        uc.addWidget(self.lbl_user_nombre)
        self.lbl_user_rol = QLabel("—")
        self.lbl_user_rol.setStyleSheet(
            "color: #C8D4E5; font-size: 11px; "
            "background: transparent; border: none;"
        )
        uc.addWidget(self.lbl_user_rol)
        user_wrapper.addWidget(self.user_card)
        sb.addLayout(user_wrapper)

        btn_logout = QPushButton("⤴  Cerrar sesión")
        btn_logout.setStyleSheet("""
            QPushButton {
                color: #C8D4E5; background-color: transparent;
                border: none; padding: 12px 20px; text-align: left;
                font-size: 13px;
            }
            QPushButton:hover { color: #FFFFFF; background-color: rgba(217,45,32,0.3); }
        """)
        btn_logout.setCursor(Qt.PointingHandCursor)
        btn_logout.clicked.connect(self._cerrar_sesion)
        sb.addWidget(btn_logout)
        sb.addStretch()

        # ===== Área de contenido =====
        self.content_area = QFrame()
        self.content_area.setStyleSheet("background-color: #F4F8FB;")
        ca = QVBoxLayout(self.content_area)
        ca.setContentsMargins(0, 0, 0, 0)
        ca.setSpacing(0)

        # Barra superior
        topbar = QFrame()
        topbar.setObjectName("header")
        topbar.setFixedHeight(56)
        tb = QHBoxLayout(topbar)
        tb.setContentsMargins(40, 0, 40, 0)
        self.lbl_titulo_pagina = QLabel("Inicio")
        self.lbl_titulo_pagina.setStyleSheet(
            "color: #102A43; font-size: 16px; font-weight: 700;"
        )
        tb.addWidget(self.lbl_titulo_pagina)
        tb.addStretch()
        self.lbl_chip = QLabel("● En línea")
        self.lbl_chip.setStyleSheet(
            "background-color: #E5F4EA; color: #16812C; "
            "padding: 4px 12px; border-radius: 10px; font-size: 11px; font-weight: 600;"
        )
        tb.addWidget(self.lbl_chip)
        ca.addWidget(topbar)

        # Stack de páginas
        self.stack = QStackedWidget()
        self.dashboard = DashboardView(self._emergency)
        self.form_view = EmergencyFormView(self._emergency)
        self.list_view = EmergencyListView(self._emergency)
        self.stack.addWidget(self.dashboard)   # 0
        self.stack.addWidget(self.form_view)   # 1
        self.stack.addWidget(self.list_view)   # 2
        ca.addWidget(self.stack)

        # Conexiones entre vistas
        self.dashboard.ir_a_registrar.connect(lambda: self.ir_a(self.PAG_FORM))
        self.dashboard.ir_a_listado.connect(lambda: self.ir_a(self.PAG_LIST))
        self.form_view.cancelado.connect(lambda: self.ir_a(self.PAG_DASH))
        self.form_view.emergencia_registrada.connect(
            lambda: self.ir_a(self.PAG_LIST)
        )
        self.list_view.cambio_realizado.connect(self.dashboard.refrescar)

        root.addWidget(self.sidebar)
        root.addWidget(self.content_area, 1)

    def _mk_sidebar_section(self, texto: str) -> QLabel:
        l = QLabel(texto)
        l.setStyleSheet(
            "color: #6B85A8; font-size: 10px; font-weight: 700; "
            "letter-spacing: 1.4px; padding: 8px 24px 6px 24px;"
        )
        return l

    def _mk_sidebar_btn(self, texto: str, on_click) -> QPushButton:
        b = QPushButton(texto)
        b.setCheckable(True)
        b.setStyleSheet("""
            QPushButton {
                color: #C8D4E5; background-color: transparent;
                border: none; padding: 12px 24px; text-align: left;
                font-size: 13px; border-left: 3px solid transparent;
            }
            QPushButton:hover {
                color: #FFFFFF; background-color: rgba(0,90,156,0.4);
            }
            QPushButton:checked {
                color: #FFFFFF; background-color: rgba(0,90,156,0.6);
                border-left: 3px solid #22A63A; font-weight: 600;
            }
        """)
        b.setCursor(Qt.PointingHandCursor)
        b.clicked.connect(on_click)
        return b

    # ---- API pública ----
    def set_usuario(self, usuario: Usuario) -> None:
        self._usuario = usuario
        self.lbl_user_nombre.setText(usuario.nombre)
        rol = "Administrador" if usuario.rol == Rol.ADMIN else "Vecino"
        self.lbl_user_rol.setText(f"{rol}  ·  {usuario.rut}")

        self.dashboard.set_usuario(usuario)
        self.form_view.set_usuario(usuario)
        self.list_view.set_usuario(usuario)

        self.dashboard.refrescar()
        self.list_view.refrescar()
        self.ir_a(self.PAG_DASH)

    def ir_a(self, indice: int) -> None:
        self.stack.setCurrentIndex(indice)
        for b in (self.btn_dash, self.btn_form, self.btn_list):
            b.setChecked(False)
        if indice == self.PAG_DASH:
            self.btn_dash.setChecked(True)
            self.lbl_titulo_pagina.setText("Inicio")
            self.dashboard.refrescar()
        elif indice == self.PAG_FORM:
            self.btn_form.setChecked(True)
            self.lbl_titulo_pagina.setText("Reportar emergencia")
        elif indice == self.PAG_LIST:
            self.btn_list.setChecked(True)
            self.lbl_titulo_pagina.setText("Reportes de emergencia")
            self.list_view.refrescar()

    def _cerrar_sesion(self) -> None:
        self._auth.logout()
        self._on_logout()
