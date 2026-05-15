"""Vista de administración para registrar usuarios reales."""

from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.controllers.user_controller import UserController
from src.widgets.buttons import estilizar_boton


class UserFormView(QWidget):
    """Formulario básico para crear vecinos o administradores."""

    def __init__(self, controller: UserController | None = None) -> None:
        super().__init__()
        self._controller = controller or UserController()
        self._build_ui()

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(40, 32, 40, 32)
        outer.setSpacing(20)

        title = QLabel("Registrar usuario")
        title.setObjectName("h1")
        outer.addWidget(title)

        sub = QLabel(
            "Crea una cuenta real para que el vecino o administrador pueda "
            "ingresar con RUT y contraseña."
        )
        sub.setStyleSheet("color: #52616B; font-size: 13px;")
        sub.setWordWrap(True)
        outer.addWidget(sub)
        outer.addSpacing(8)

        card = QFrame()
        card.setObjectName("card")
        card_lay = QVBoxLayout(card)
        card_lay.setContentsMargins(28, 24, 28, 24)
        card_lay.setSpacing(14)

        fila_identidad = QHBoxLayout()
        fila_identidad.setSpacing(16)

        col_rut = QVBoxLayout()
        col_rut.setSpacing(6)
        col_rut.addWidget(self._lbl("RUT *"))
        self.input_rut = QLineEdit()
        self.input_rut.setPlaceholderText("Ej: 12.345.678-5")
        col_rut.addWidget(self.input_rut)
        fila_identidad.addLayout(col_rut)

        col_rol = QVBoxLayout()
        col_rol.setSpacing(6)
        col_rol.addWidget(self._lbl("Rol *"))
        self.cb_rol = QComboBox()
        self.cb_rol.addItem("Vecino", 2)
        self.cb_rol.addItem("Administrador", 1)
        col_rol.addWidget(self.cb_rol)
        fila_identidad.addLayout(col_rol)
        card_lay.addLayout(fila_identidad)

        card_lay.addWidget(self._lbl("Nombre completo *"))
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Ej: Nuevo Vecino")
        card_lay.addWidget(self.input_nombre)

        card_lay.addWidget(self._lbl("Email *"))
        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Ej: nuevo.vecino@vecinoseguro.cl")
        card_lay.addWidget(self.input_email)

        card_lay.addWidget(self._lbl("Contraseña inicial *"))
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Mínimo 6 caracteres")
        self.input_password.setEchoMode(QLineEdit.Password)
        card_lay.addWidget(self.input_password)

        nota = QLabel(
            "La contraseña se envía al backend y se almacena como hash bcrypt. "
            "No se muestra ni guarda en la aplicación desktop."
        )
        nota.setStyleSheet(
            "background-color: #E5F0FB; color: #005A9C; "
            "padding: 10px 14px; border-radius: 6px; font-size: 12px;"
        )
        nota.setWordWrap(True)
        card_lay.addWidget(nota)
        outer.addWidget(card)

        botones = QHBoxLayout()
        botones.addStretch()
        btn_limpiar = QPushButton("Limpiar")
        estilizar_boton(btn_limpiar, "secondary")
        btn_limpiar.clicked.connect(self.limpiar)
        botones.addWidget(btn_limpiar)

        self.btn_guardar = QPushButton("Guardar usuario")
        estilizar_boton(self.btn_guardar, "success")
        self.btn_guardar.clicked.connect(self._guardar)
        botones.addWidget(self.btn_guardar)
        outer.addLayout(botones)
        outer.addStretch()

    def _lbl(self, texto: str) -> QLabel:
        label = QLabel(texto)
        label.setStyleSheet("color: #52616B; font-weight: 600; font-size: 12px;")
        return label

    def limpiar(self) -> None:
        self.input_rut.clear()
        self.input_nombre.clear()
        self.input_email.clear()
        self.input_password.clear()
        self.cb_rol.setCurrentIndex(0)

    def _guardar(self) -> None:
        self.btn_guardar.setEnabled(False)
        self.btn_guardar.setText("Guardando...")
        try:
            ok, msg, creado = self._controller.crear_usuario(
                rut=self.input_rut.text(),
                full_name=self.input_nombre.text(),
                email=self.input_email.text(),
                password=self.input_password.text(),
                role_id=int(self.cb_rol.currentData()),
            )
            if ok:
                nombre = creado.get("full_name", "Usuario") if creado else "Usuario"
                QMessageBox.information(
                    self,
                    "Usuario creado",
                    f"{nombre} fue registrado correctamente.",
                )
                self.limpiar()
            else:
                QMessageBox.warning(self, "No fue posible crear el usuario", msg)
        finally:
            self.btn_guardar.setEnabled(True)
            self.btn_guardar.setText("Guardar usuario")
