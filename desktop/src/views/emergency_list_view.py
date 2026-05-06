"""Vista de listado de reportes con detalle integrado.

Presenta los reportes en una tabla filtrable. Al seleccionar una fila se
muestra el detalle del reporte. Si el usuario es administrador, se habilita
un panel para cambiar el estado y agregar observaciones.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSplitter,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.controllers.emergency_controller import EmergencyController
from src.models.entities import EstadoEmergencia, Rol, Usuario
from src.widgets.badges import estilizar_badge_estado, estilizar_badge_urgencia
from src.widgets.buttons import estilizar_boton


class EmergencyListView(QWidget):
    """Listado tabular con detalle y panel admin embebido."""

    cambio_realizado = Signal()

    def __init__(self, controller: EmergencyController) -> None:
        super().__init__()
        self.setWindowTitle("VecinoSeguro · Reportes")
        self._controller = controller
        self._usuario: Usuario | None = None
        self._emergencia_seleccionada_id: int | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(40, 32, 40, 32)
        outer.setSpacing(18)

        # Header
        h = QHBoxLayout()
        title = QLabel("Reportes de emergencia")
        title.setObjectName("h1")
        h.addWidget(title)
        h.addStretch()
        self.btn_refrescar = QPushButton("↻  Actualizar")
        estilizar_boton(self.btn_refrescar, "secondary")
        self.btn_refrescar.clicked.connect(self.refrescar)
        h.addWidget(self.btn_refrescar)
        outer.addLayout(h)

        # Filtros
        filtros = QFrame()
        filtros.setObjectName("card")
        f_lay = QHBoxLayout(filtros)
        f_lay.setContentsMargins(16, 12, 16, 12)
        f_lay.setSpacing(12)
        f_lay.addWidget(self._lbl_inline("Filtrar por estado:"))
        self.cb_filtro = QComboBox()
        self.cb_filtro.addItem("Todos", None)
        for est in EstadoEmergencia:
            self.cb_filtro.addItem(est.value, est)
        self.cb_filtro.currentIndexChanged.connect(self.refrescar)
        f_lay.addWidget(self.cb_filtro)
        f_lay.addStretch()
        self.lbl_total = QLabel("0 reportes")
        self.lbl_total.setStyleSheet("color: #52616B; font-size: 12px;")
        f_lay.addWidget(self.lbl_total)
        outer.addWidget(filtros)

        # Splitter: tabla + detalle
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(8)

        # === Tabla ===
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(
            ["#", "Tipo", "Ubicación", "Urgencia", "Estado", "Fecha"]
        )
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.setAlternatingRowColors(False)
        self.tabla.itemSelectionChanged.connect(self._on_seleccion)
        h_header = self.tabla.horizontalHeader()
        h_header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        h_header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        h_header.setSectionResizeMode(2, QHeaderView.Stretch)
        h_header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        h_header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        h_header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.tabla.setMinimumWidth(560)
        splitter.addWidget(self.tabla)

        # === Detalle ===
        self.detalle_stack = QStackedWidget()

        # Estado vacío
        vacio = QFrame()
        vacio.setObjectName("card")
        vacio_lay = QVBoxLayout(vacio)
        vacio_lay.setContentsMargins(24, 24, 24, 24)
        vacio_lay.addStretch()
        icono = QLabel("📋")
        icono.setStyleSheet("font-size: 40px; background: transparent;")
        icono.setAlignment(Qt.AlignCenter)
        vacio_lay.addWidget(icono)
        msg = QLabel("Selecciona un reporte\npara ver el detalle")
        msg.setStyleSheet("color: #52616B; font-size: 13px; background: transparent;")
        msg.setAlignment(Qt.AlignCenter)
        vacio_lay.addWidget(msg)
        vacio_lay.addStretch()
        self.detalle_stack.addWidget(vacio)

        # Panel real (envuelto en scroll para que el panel admin nunca se corte)
        self.panel_detalle = self._build_detalle_panel()
        scroll_detalle = QScrollArea()
        scroll_detalle.setWidget(self.panel_detalle)
        scroll_detalle.setWidgetResizable(True)
        scroll_detalle.setFrameShape(QScrollArea.NoFrame)
        scroll_detalle.setStyleSheet(
            "QScrollArea { background: transparent; border: none; }"
        )
        self.detalle_stack.addWidget(scroll_detalle)
        self.detalle_stack.setMinimumWidth(360)

        splitter.addWidget(self.detalle_stack)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)
        outer.addWidget(splitter, 1)

    def _build_detalle_panel(self) -> QFrame:
        f = QFrame()
        f.setObjectName("card")
        lay = QVBoxLayout(f)
        lay.setContentsMargins(22, 20, 22, 20)
        lay.setSpacing(10)

        head = QHBoxLayout()
        self.lbl_id = QLabel("#000")
        self.lbl_id.setStyleSheet("color: #52616B; font-size: 12px; font-weight: 600;")
        head.addWidget(self.lbl_id)
        head.addStretch()
        self.lbl_estado_badge = QLabel("")
        head.addWidget(self.lbl_estado_badge)
        lay.addLayout(head)

        self.lbl_tipo = QLabel("Tipo")
        self.lbl_tipo.setStyleSheet("font-size: 20px; font-weight: 700; color: #073B6B;")
        self.lbl_tipo.setWordWrap(True)
        lay.addWidget(self.lbl_tipo)

        self.lbl_urg_badge = QLabel("")
        head_urg = QHBoxLayout()
        head_urg.addWidget(self.lbl_urg_badge)
        head_urg.addStretch()
        lay.addLayout(head_urg)
        lay.addSpacing(8)

        self.lbl_ubicacion  = self._mk_field("Ubicación", "—")
        self.lbl_reportante = self._mk_field("Reportado por", "—")
        self.lbl_fecha      = self._mk_field("Fecha de reporte", "—")
        for w in (self.lbl_ubicacion, self.lbl_reportante, self.lbl_fecha):
            lay.addWidget(w)

        lay.addSpacing(8)
        lay.addWidget(self._mk_section_title("Descripción"))
        self.lbl_descripcion = QLabel("—")
        self.lbl_descripcion.setWordWrap(True)
        self.lbl_descripcion.setStyleSheet(
            "background-color: #F4F8FB; padding: 12px; border-radius: 6px; "
            "color: #102A43; font-size: 13px;"
        )
        lay.addWidget(self.lbl_descripcion)

        lay.addSpacing(8)
        self.lbl_obs_title = self._mk_section_title("Observaciones del administrador")
        lay.addWidget(self.lbl_obs_title)
        self.lbl_obs = QLabel("—")
        self.lbl_obs.setWordWrap(True)
        self.lbl_obs.setStyleSheet(
            "background-color: #F4F8FB; padding: 12px; border-radius: 6px; "
            "color: #52616B; font-size: 12px; font-style: italic;"
        )
        lay.addWidget(self.lbl_obs)

        # Panel de admin (visible solo para administradores)
        self.admin_panel = QFrame()
        self.admin_panel.setObjectName("adminPanel")
        adm_lay = QVBoxLayout(self.admin_panel)
        adm_lay.setContentsMargins(16, 14, 16, 14)
        adm_lay.setSpacing(10)
        t_admin = QLabel("⚙ Acciones del administrador")
        t_admin.setStyleSheet(
            "color: #92400E; font-weight: 700; font-size: 12px; "
            "background: transparent; border: none;"
        )
        adm_lay.addWidget(t_admin)

        cambio_row = QVBoxLayout()
        cambio_row.setSpacing(4)
        lbl_e = QLabel("Cambiar estado a:")
        lbl_e.setStyleSheet(
            "color: #52616B; font-size: 11px; font-weight: 600; "
            "background: transparent; border: none;"
        )
        cambio_row.addWidget(lbl_e)
        self.cb_nuevo_estado = QComboBox()
        for est in EstadoEmergencia:
            self.cb_nuevo_estado.addItem(est.value, est)
        cambio_row.addWidget(self.cb_nuevo_estado)
        adm_lay.addLayout(cambio_row)

        lbl_o = QLabel("Observación (opcional):")
        lbl_o.setStyleSheet(
            "color: #52616B; font-size: 11px; font-weight: 600; "
            "background: transparent; border: none;"
        )
        adm_lay.addWidget(lbl_o)
        self.input_obs = QTextEdit()
        self.input_obs.setMaximumHeight(60)
        self.input_obs.setPlaceholderText(
            "Notas internas para el seguimiento del reporte…"
        )
        adm_lay.addWidget(self.input_obs)

        self.btn_actualizar = QPushButton("Actualizar estado")
        estilizar_boton(self.btn_actualizar, "primary")
        self.btn_actualizar.clicked.connect(self._actualizar_estado)
        adm_lay.addWidget(self.btn_actualizar)
        lay.addWidget(self.admin_panel)
        lay.addStretch()
        return f

    # ---- helpers ----
    def _mk_field(self, etiqueta: str, valor: str) -> QFrame:
        wrapper = QFrame()
        wlay = QVBoxLayout(wrapper)
        wlay.setContentsMargins(0, 0, 0, 0)
        wlay.setSpacing(2)
        l1 = QLabel(etiqueta)
        l1.setStyleSheet(
            "color: #52616B; font-size: 10px; font-weight: 700; "
            "text-transform: uppercase; letter-spacing: 0.6px;"
        )
        l2 = QLabel(valor)
        l2.setStyleSheet("color: #102A43; font-size: 13px;")
        l2.setWordWrap(True)
        wlay.addWidget(l1)
        wlay.addWidget(l2)
        wrapper.setProperty("value_label", l2)
        return wrapper

    def _mk_section_title(self, texto: str) -> QLabel:
        l = QLabel(texto)
        l.setStyleSheet(
            "color: #52616B; font-size: 10px; font-weight: 700; "
            "text-transform: uppercase; letter-spacing: 0.6px;"
        )
        return l

    def _lbl_inline(self, texto: str) -> QLabel:
        l = QLabel(texto)
        l.setStyleSheet("color: #52616B; font-size: 12px; font-weight: 600;")
        return l

    # ---- API pública ----
    def set_usuario(self, usuario: Usuario) -> None:
        self._usuario = usuario
        es_admin = usuario.rol == Rol.ADMIN
        self.admin_panel.setVisible(es_admin)
        self.lbl_obs_title.setVisible(es_admin)
        self.lbl_obs.setVisible(es_admin)

    def refrescar(self) -> None:
        filtro: EstadoEmergencia | None = self.cb_filtro.currentData()
        emergencias = (
            self._controller.listar() if filtro is None
            else self._controller.listar_por_estado(filtro)
        )
        self.lbl_total.setText(f"{len(emergencias)} reporte(s)")

        self.tabla.setRowCount(len(emergencias))
        for row, em in enumerate(emergencias):
            self._set_cell(row, 0, f"#{em.id}", align=Qt.AlignCenter,
                           color="#52616B", weight=600, data=em.id)
            self._set_cell(row, 1, em.tipo.value)
            self._set_cell(row, 2, em.ubicacion)
            self._set_cell(row, 3, em.nivel_urgencia.value, align=Qt.AlignCenter,
                           color=self._color_urg(em.nivel_urgencia.value), weight=700)
            self._set_cell(row, 4, em.estado.value, align=Qt.AlignCenter,
                           color=self._color_est(em.estado.value), weight=600)
            self._set_cell(row, 5, em.fecha_reporte.strftime("%d-%m-%Y %H:%M"),
                           align=Qt.AlignCenter, color="#52616B")

        for r in range(self.tabla.rowCount()):
            self.tabla.setRowHeight(r, 38)

        # Mantener selección si el id sigue presente
        if self._emergencia_seleccionada_id is not None:
            for r in range(self.tabla.rowCount()):
                item = self.tabla.item(r, 0)
                if item and item.data(Qt.UserRole) == self._emergencia_seleccionada_id:
                    self.tabla.selectRow(r)
                    return
        self._emergencia_seleccionada_id = None
        self.detalle_stack.setCurrentIndex(0)

    def _set_cell(self, row, col, texto, align=Qt.AlignLeft | Qt.AlignVCenter,
                  color: str | None = None, weight: int = 400, data=None) -> None:
        item = QTableWidgetItem(texto)
        item.setTextAlignment(align)
        if color:
            item.setForeground(QColor(color))
        f = QFont()
        if weight >= 700:
            f.setWeight(QFont.Weight.Bold)
        elif weight >= 600:
            f.setWeight(QFont.Weight.DemiBold)
        else:
            f.setWeight(QFont.Weight.Normal)
        item.setFont(f)
        if data is not None:
            item.setData(Qt.UserRole, data)
        self.tabla.setItem(row, col, item)

    def _color_urg(self, v: str) -> str:
        return {"Crítica": "#9B2C2C", "Alta": "#C05621",
                "Media": "#975A16", "Baja": "#22543D"}.get(v, "#102A43")

    def _color_est(self, v: str) -> str:
        return {"Pendiente": "#F2A900", "En revisión": "#005A9C",
                "Atendido": "#16812C", "Resuelto": "#52616B"}.get(v, "#102A43")

    # ---- Detalle ----
    def _on_seleccion(self) -> None:
        rows = self.tabla.selectionModel().selectedRows()
        if not rows:
            self.detalle_stack.setCurrentIndex(0)
            self._emergencia_seleccionada_id = None
            return
        row = rows[0].row()
        item_id = self.tabla.item(row, 0)
        if item_id:
            self._mostrar_detalle(item_id.data(Qt.UserRole))

    def _mostrar_detalle(self, emergencia_id: int) -> None:
        em = self._controller.obtener(emergencia_id)
        if not em:
            self.detalle_stack.setCurrentIndex(0)
            return
        self._emergencia_seleccionada_id = em.id

        self.lbl_id.setText(f"REPORTE #{em.id}")
        self.lbl_tipo.setText(em.tipo.value)

        # Badges mediante widgets reutilizables
        estilizar_badge_estado(self.lbl_estado_badge, em.estado.value)
        estilizar_badge_urgencia(self.lbl_urg_badge, em.nivel_urgencia.value)

        self.lbl_ubicacion.property("value_label").setText(em.ubicacion)
        self.lbl_reportante.property("value_label").setText(
            f"{em.nombre_reportante}  ·  {em.rut_reportante}"
        )
        self.lbl_fecha.property("value_label").setText(
            em.fecha_reporte.strftime("%d-%m-%Y a las %H:%M hrs")
        )
        self.lbl_descripcion.setText(em.descripcion)

        es_admin = self._usuario and self._usuario.rol == Rol.ADMIN
        if em.observaciones:
            self.lbl_obs.setText(em.observaciones)
            self.lbl_obs_title.setVisible(True)
            self.lbl_obs.setVisible(True)
        else:
            self.lbl_obs.setText("Sin observaciones aún.")
            self.lbl_obs_title.setVisible(es_admin)
            self.lbl_obs.setVisible(es_admin)

        idx = self.cb_nuevo_estado.findData(em.estado)
        if idx >= 0:
            self.cb_nuevo_estado.setCurrentIndex(idx)
        self.input_obs.setPlainText(em.observaciones)

        self.detalle_stack.setCurrentIndex(1)

    def _actualizar_estado(self) -> None:
        if self._emergencia_seleccionada_id is None:
            return
        ok, msg = self._controller.cambiar_estado(
            self._emergencia_seleccionada_id,
            self.cb_nuevo_estado.currentData(),
            self.input_obs.toPlainText().strip(),
        )
        if ok:
            QMessageBox.information(self, "Estado actualizado", msg)
            self.cambio_realizado.emit()
            self.refrescar()
            self._mostrar_detalle(self._emergencia_seleccionada_id)
        else:
            QMessageBox.warning(self, "Error", msg)
