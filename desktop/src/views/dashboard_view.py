"""Vista del panel principal (dashboard).

Muestra un resumen visual de las emergencias agrupadas por estado, accesos
rápidos a las acciones más usadas y los reportes más recientes. Toda la
información se obtiene a través del `EmergencyController`.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from src.controllers.emergency_controller import EmergencyController
from src.models.entities import EstadoEmergencia, Usuario
from src.widgets.badges import crear_badge_estado


class DashboardView(QWidget):
    """Panel principal con estadísticas y atajos."""

    ir_a_registrar = Signal()
    ir_a_listado = Signal()

    def __init__(self, emergency_controller: EmergencyController) -> None:
        super().__init__()
        self.setWindowTitle("VecinoSeguro · Panel")
        self._controller = emergency_controller
        self._usuario: Usuario | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 32, 40, 32)
        layout.setSpacing(24)

        bienvenida_box = QVBoxLayout()
        bienvenida_box.setSpacing(4)
        self.lbl_bienvenida = QLabel("Hola")
        self.lbl_bienvenida.setObjectName("h1")
        bienvenida_box.addWidget(self.lbl_bienvenida)

        self.lbl_subtitulo = QLabel("Bienvenido a tu panel comunitario")
        self.lbl_subtitulo.setStyleSheet("color: #52616B; font-size: 14px;")
        bienvenida_box.addWidget(self.lbl_subtitulo)
        layout.addLayout(bienvenida_box)

        # ---- KPIs ----
        kpi_grid = QGridLayout()
        kpi_grid.setSpacing(18)
        self.kpi_pendientes = self._mk_kpi("0", "Pendientes",  "#F2A900")
        self.kpi_revision   = self._mk_kpi("0", "En revisión", "#005A9C")
        self.kpi_atendidos  = self._mk_kpi("0", "Atendidos",   "#22A63A")
        self.kpi_resueltos  = self._mk_kpi("0", "Resueltos",   "#52616B")
        kpi_grid.addWidget(self.kpi_pendientes[0], 0, 0)
        kpi_grid.addWidget(self.kpi_revision[0],   0, 1)
        kpi_grid.addWidget(self.kpi_atendidos[0],  0, 2)
        kpi_grid.addWidget(self.kpi_resueltos[0],  0, 3)
        layout.addLayout(kpi_grid)

        # ---- Acciones rápidas ----
        acciones_titulo = QLabel("Acciones rápidas")
        acciones_titulo.setObjectName("h2")
        layout.addWidget(acciones_titulo)

        acciones_layout = QHBoxLayout()
        acciones_layout.setSpacing(14)
        acciones_layout.addWidget(self._mk_action_card(
            "🚨", "Reportar emergencia",
            "Registra un incidente en tu comunidad",
            "#22A63A", self.ir_a_registrar.emit,
        ))
        acciones_layout.addWidget(self._mk_action_card(
            "📋", "Ver todos los reportes",
            "Revisa el listado completo de incidentes",
            "#005A9C", self.ir_a_listado.emit,
        ))
        layout.addLayout(acciones_layout)

        # ---- Reportes recientes ----
        recientes_titulo = QLabel("Reportes recientes")
        recientes_titulo.setObjectName("h2")
        layout.addWidget(recientes_titulo)

        self.recientes_box = QVBoxLayout()
        self.recientes_box.setSpacing(8)
        self.recientes_container = QFrame()
        self.recientes_container.setLayout(self.recientes_box)
        layout.addWidget(self.recientes_container)
        layout.addStretch()

    # ---- Helpers de construcción de tarjetas ----
    def _mk_kpi(self, numero: str, etiqueta: str, color: str) -> tuple[QFrame, QLabel]:
        card = QFrame()
        card.setObjectName("kpiCard")
        card.setMinimumHeight(110)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(20, 16, 20, 16)
        lay.setSpacing(4)
        lbl_num = QLabel(numero)
        lbl_num.setStyleSheet(f"font-size: 38px; font-weight: 800; color: {color};")
        lay.addWidget(lbl_num)
        lbl_txt = QLabel(etiqueta)
        lbl_txt.setObjectName("kpiLabel")
        lay.addWidget(lbl_txt)
        return card, lbl_num

    def _mk_action_card(self, icono: str, titulo: str, descripcion: str,
                        color: str, on_click) -> QFrame:
        card = QFrame()
        card.setObjectName("actionCard")
        card.setMinimumHeight(110)
        card.setCursor(Qt.PointingHandCursor)
        lay = QHBoxLayout(card)
        lay.setContentsMargins(20, 16, 20, 16)
        lay.setSpacing(16)

        icon_lbl = QLabel(icono)
        icon_lbl.setStyleSheet(
            f"background-color: {color}; color: white; font-size: 20px; "
            f"border-radius: 24px; min-width: 48px; min-height: 48px; "
            f"max-width: 48px; max-height: 48px; border: none;"
        )
        icon_lbl.setAlignment(Qt.AlignCenter)
        lay.addWidget(icon_lbl)

        text_box = QVBoxLayout()
        text_box.setSpacing(2)
        t = QLabel(titulo)
        t.setStyleSheet(
            "font-size: 15px; font-weight: 700; color: #102A43; "
            "background: transparent; border: none;"
        )
        text_box.addWidget(t)
        d = QLabel(descripcion)
        d.setStyleSheet(
            "font-size: 12px; color: #52616B; background: transparent; border: none;"
        )
        d.setWordWrap(True)
        text_box.addWidget(d)
        lay.addLayout(text_box)
        lay.addStretch()

        card.mousePressEvent = lambda ev: on_click()
        return card

    def _mk_reciente_row(self, emergencia) -> QFrame:
        f = QFrame()
        f.setObjectName("recentRow")
        l = QHBoxLayout(f)
        l.setContentsMargins(16, 12, 16, 12)
        l.setSpacing(12)

        color_urg = {
            "Crítica": "#D92D20", "Alta": "#F2A900",
            "Media": "#D69E2E",   "Baja": "#22A63A",
        }.get(emergencia.nivel_urgencia.value, "#52616B")
        dot = QLabel()
        dot.setStyleSheet(
            f"background-color: {color_urg}; border-radius: 5px; "
            f"min-width: 10px; max-width: 10px; min-height: 10px; max-height: 10px; "
            f"border: none;"
        )
        l.addWidget(dot)

        text_box = QVBoxLayout()
        text_box.setSpacing(2)
        titulo = QLabel(f"{emergencia.tipo.value} · {emergencia.ubicacion}")
        titulo.setStyleSheet(
            "font-size: 13px; font-weight: 600; color: #102A43; "
            "background: transparent; border: none;"
        )
        text_box.addWidget(titulo)
        meta = QLabel(
            f"#{emergencia.id} · {emergencia.nombre_reportante} · "
            f"{emergencia.fecha_reporte.strftime('%d-%m-%Y %H:%M')}"
        )
        meta.setStyleSheet(
            "font-size: 11px; color: #52616B; background: transparent; border: none;"
        )
        text_box.addWidget(meta)
        l.addLayout(text_box)
        l.addStretch()

        # Badge de estado mediante widget reutilizable
        badge = crear_badge_estado(emergencia.estado.value)
        l.addWidget(badge)
        return f

    # ---- API pública ----
    def set_usuario(self, usuario: Usuario) -> None:
        self._usuario = usuario
        nombre_corto = usuario.nombre.split()[0]
        self.lbl_bienvenida.setText(f"Hola, {nombre_corto} 👋")
        rol_texto = "Administrador" if usuario.rol.value == "admin" else "Vecino"
        self.lbl_subtitulo.setText(f"Sesión iniciada como {rol_texto}")

    def refrescar(self) -> None:
        stats = self._controller.estadisticas()
        self.kpi_pendientes[1].setText(str(stats[EstadoEmergencia.PENDIENTE]))
        self.kpi_revision[1].setText(str(stats[EstadoEmergencia.EN_REVISION]))
        self.kpi_atendidos[1].setText(str(stats[EstadoEmergencia.ATENDIDO]))
        self.kpi_resueltos[1].setText(str(stats[EstadoEmergencia.RESUELTO]))

        # Limpiar y recargar las filas de reportes recientes
        while self.recientes_box.count():
            item = self.recientes_box.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        recientes = self._controller.listar()[:4]
        if not recientes:
            vacio = QLabel("No hay reportes aún.")
            vacio.setStyleSheet("color: #9CA3AF; padding: 24px; font-style: italic;")
            vacio.setAlignment(Qt.AlignCenter)
            self.recientes_box.addWidget(vacio)
            return

        for em in recientes:
            self.recientes_box.addWidget(self._mk_reciente_row(em))
