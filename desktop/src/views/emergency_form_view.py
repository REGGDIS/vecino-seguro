"""Vista de formulario para registrar emergencias.

Permite al vecino reportar un nuevo incidente. Las validaciones de negocio
viven en `EmergencyController.registrar`; la vista solo recolecta los datos
y muestra el resultado al usuario.
"""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.controllers.emergency_controller import EmergencyController
from src.models.entities import NivelUrgencia, TipoEmergencia, Usuario
from src.views.ui_helpers import estilizar_boton


class EmergencyFormView(QWidget):
    """Formulario de registro de un nuevo reporte de emergencia."""

    emergencia_registrada = Signal()
    cancelado = Signal()

    def __init__(self, controller: EmergencyController) -> None:
        super().__init__()
        self.setWindowTitle("VecinoSeguro · Registrar emergencia")
        self._controller = controller
        self._usuario: Usuario | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(40, 32, 40, 32)
        outer.setSpacing(20)

        title = QLabel("Reportar emergencia")
        title.setObjectName("h1")
        outer.addWidget(title)
        sub = QLabel(
            "Completa los siguientes datos para que la comunidad y el "
            "administrador puedan revisar tu reporte."
        )
        sub.setStyleSheet("color: #6B7280; font-size: 13px;")
        sub.setWordWrap(True)
        outer.addWidget(sub)
        outer.addSpacing(8)

        card = QFrame()
        card.setObjectName("card")
        card_lay = QVBoxLayout(card)
        card_lay.setContentsMargins(28, 24, 28, 24)
        card_lay.setSpacing(14)

        # Tipo + Urgencia (2 columnas)
        fila1 = QHBoxLayout()
        fila1.setSpacing(16)

        col_tipo = QVBoxLayout()
        col_tipo.setSpacing(6)
        col_tipo.addWidget(self._lbl("Tipo de emergencia *"))
        self.cb_tipo = QComboBox()
        for t in TipoEmergencia:
            self.cb_tipo.addItem(t.value, t)
        col_tipo.addWidget(self.cb_tipo)
        fila1.addLayout(col_tipo)

        col_urg = QVBoxLayout()
        col_urg.setSpacing(6)
        col_urg.addWidget(self._lbl("Nivel de urgencia *"))
        self.cb_urg = QComboBox()
        for u in NivelUrgencia:
            self.cb_urg.addItem(u.value, u)
        self.cb_urg.setCurrentText(NivelUrgencia.MEDIA.value)
        col_urg.addWidget(self.cb_urg)
        fila1.addLayout(col_urg)
        card_lay.addLayout(fila1)

        card_lay.addWidget(self._lbl("Ubicación referencial *"))
        self.input_ubicacion = QLineEdit()
        self.input_ubicacion.setPlaceholderText(
            "Ej: Av. Los Carrera con Lautaro, frente al almacén"
        )
        card_lay.addWidget(self.input_ubicacion)

        card_lay.addWidget(self._lbl("Descripción del incidente *"))
        self.input_desc = QTextEdit()
        self.input_desc.setPlaceholderText(
            "Describe lo que está ocurriendo con el mayor detalle posible "
            "(mínimo 10 caracteres)…"
        )
        self.input_desc.setMinimumHeight(120)
        card_lay.addWidget(self.input_desc)

        nota = QLabel(
            "ℹ La fecha y datos del reportante se completan automáticamente. "
            "El reporte queda en estado <b>Pendiente</b> hasta que un "
            "administrador lo revise."
        )
        nota.setStyleSheet(
            "background-color: #EEF3FA; color: #1B4F8C; "
            "padding: 10px 14px; border-radius: 6px; font-size: 12px;"
        )
        nota.setWordWrap(True)
        card_lay.addWidget(nota)
        outer.addWidget(card)

        botones = QHBoxLayout()
        botones.addStretch()
        btn_cancel = QPushButton("Cancelar")
        estilizar_boton(btn_cancel, "secondary")
        btn_cancel.clicked.connect(self.cancelado.emit)
        botones.addWidget(btn_cancel)

        btn_enviar = QPushButton("Registrar reporte")
        estilizar_boton(btn_enviar, "success")
        btn_enviar.clicked.connect(self._registrar)
        botones.addWidget(btn_enviar)
        outer.addLayout(botones)
        outer.addStretch()

    def _lbl(self, texto: str) -> QLabel:
        l = QLabel(texto)
        l.setStyleSheet("color: #4A5568; font-weight: 600; font-size: 12px;")
        return l

    # ---- API pública ----
    def set_usuario(self, usuario: Usuario) -> None:
        self._usuario = usuario

    def limpiar(self) -> None:
        self.cb_tipo.setCurrentIndex(0)
        self.cb_urg.setCurrentText(NivelUrgencia.MEDIA.value)
        self.input_ubicacion.clear()
        self.input_desc.clear()

    def _registrar(self) -> None:
        if not self._usuario:
            return
        ok, msg, _ = self._controller.registrar(
            usuario=self._usuario,
            tipo=self.cb_tipo.currentData(),
            descripcion=self.input_desc.toPlainText(),
            ubicacion=self.input_ubicacion.text(),
            nivel_urgencia=self.cb_urg.currentData(),
        )
        if ok:
            QMessageBox.information(self, "Reporte registrado", msg)
            self.limpiar()
            self.emergencia_registrada.emit()
        else:
            QMessageBox.warning(self, "Datos incompletos", msg)
