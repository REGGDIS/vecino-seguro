"""Vista de administración para registrar usuarios reales."""

from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

from src.controllers.user_controller import UserController
from src.widgets.buttons import estilizar_boton


class UserFormView(QWidget):
    """Formulario básico para crear vecinos o administradores."""

    def __init__(self, controller: UserController | None = None) -> None:
        super().__init__()
        self._controller = controller or UserController()
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setStyleSheet(
            "QScrollArea { background: transparent; border: none; }"
        )

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        outer = QVBoxLayout(content)
        outer.setContentsMargins(40, 32, 40, 32)
        outer.setSpacing(22)

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

        card = QFrame()
        card.setObjectName("card")
        card.setMinimumHeight(390)
        card_lay = QVBoxLayout(card)
        card_lay.setContentsMargins(28, 26, 28, 26)
        card_lay.setSpacing(18)

        fila_identidad = QHBoxLayout()
        fila_identidad.setSpacing(20)

        col_rut = QVBoxLayout()
        col_rut.setSpacing(8)
        col_rut.addWidget(self._lbl("RUT *"))
        self.input_rut = QLineEdit()
        self.input_rut.setPlaceholderText("Ej: 12.345.678-5")
        self.input_rut.setMinimumHeight(36)
        col_rut.addWidget(self.input_rut)
        fila_identidad.addLayout(col_rut, 3)

        col_rol = QVBoxLayout()
        col_rol.setSpacing(8)
        col_rol.addWidget(self._lbl("Rol *"))
        self.cb_rol = QComboBox()
        self.cb_rol.addItem("Vecino", 2)
        self.cb_rol.addItem("Administrador", 1)
        self.cb_rol.setMinimumHeight(36)
        col_rol.addWidget(self.cb_rol)
        fila_identidad.addLayout(col_rol, 1)
        card_lay.addLayout(fila_identidad)

        ayuda_roles = QLabel(
            "Vecino: puede iniciar sesión, reportar emergencias y revisar el estado de sus reportes.\n"
            "Administrador: puede gestionar reportes y registrar nuevos usuarios."
        )
        ayuda_roles.setWordWrap(True)
        ayuda_roles.setStyleSheet(
            "color: #52616B; font-size: 12px; background: transparent;"
        )
        card_lay.addWidget(ayuda_roles)

        campo_nombre = QVBoxLayout()
        campo_nombre.setSpacing(8)
        campo_nombre.addWidget(self._lbl("Nombre completo *"))
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Ej: Nuevo Vecino")
        self.input_nombre.setMinimumHeight(36)
        campo_nombre.addWidget(self.input_nombre)
        card_lay.addLayout(campo_nombre)

        campo_email = QVBoxLayout()
        campo_email.setSpacing(8)
        campo_email.addWidget(self._lbl("Email *"))
        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Ej: nuevo.vecino@vecinoseguro.cl")
        self.input_email.setMinimumHeight(36)
        campo_email.addWidget(self.input_email)
        card_lay.addLayout(campo_email)

        campo_password = QVBoxLayout()
        campo_password.setSpacing(8)
        campo_password.addWidget(self._lbl("Contraseña inicial *"))
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Mínimo 6 caracteres")
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setMinimumHeight(36)
        campo_password.addWidget(self.input_password)
        card_lay.addLayout(campo_password)

        nota = QLabel(
            "La contraseña inicial será utilizada por el usuario para iniciar sesión. "
            "Por seguridad, el sistema no la muestra ni la guarda en texto visible "
            "dentro de la aplicación desktop."
        )
        nota.setStyleSheet(
            "background-color: #E5F0FB; color: #005A9C; "
            "padding: 10px 14px; border-radius: 6px; font-size: 12px;"
        )
        nota.setWordWrap(True)
        card_lay.addWidget(nota)

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
        card_lay.addLayout(botones)
        outer.addWidget(card)

        table_card = QFrame()
        table_card.setObjectName("card")
        table_card_lay = QVBoxLayout(table_card)
        table_card_lay.setContentsMargins(24, 22, 24, 24)
        table_card_lay.setSpacing(12)

        users_header = QHBoxLayout()
        users_header.setSpacing(12)
        users_title = QLabel("Usuarios registrados")
        users_title.setObjectName("h1")
        users_header.addWidget(users_title)
        users_header.addStretch()
        self.btn_refrescar = QPushButton("Actualizar listado")
        estilizar_boton(self.btn_refrescar, "secondary")
        self.btn_refrescar.clicked.connect(self.refrescar)
        users_header.addWidget(self.btn_refrescar)
        table_card_lay.addLayout(users_header)

        self.lbl_estado_listado = QLabel("Listado pendiente de cargar.")
        self.lbl_estado_listado.setStyleSheet("color: #52616B; font-size: 12px;")
        table_card_lay.addWidget(self.lbl_estado_listado)

        self.tabla_usuarios = QTableWidget()
        self.tabla_usuarios.setColumnCount(5)
        self.tabla_usuarios.setHorizontalHeaderLabels(
            ["ID", "RUT", "Nombre", "Email", "Rol"]
        )
        self.tabla_usuarios.verticalHeader().setVisible(False)
        self.tabla_usuarios.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_usuarios.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla_usuarios.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_usuarios.setAlternatingRowColors(False)
        header = self.tabla_usuarios.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.tabla_usuarios.setMinimumHeight(240)
        table_card_lay.addWidget(self.tabla_usuarios)
        outer.addWidget(table_card)
        outer.addStretch()

        scroll.setWidget(content)
        root.addWidget(scroll)

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

    def refrescar(self) -> None:
        self.btn_refrescar.setEnabled(False)
        self.lbl_estado_listado.setText("Cargando usuarios registrados...")
        try:
            ok, msg, usuarios = self._controller.listar_usuarios()
            if not ok:
                self.tabla_usuarios.setRowCount(0)
                self.lbl_estado_listado.setText(msg)
                return

            self._cargar_tabla(usuarios)
            if usuarios:
                self.lbl_estado_listado.setText(
                    f"{len(usuarios)} usuario(s) registrado(s)."
                )
            else:
                self.lbl_estado_listado.setText("No hay usuarios registrados.")
        finally:
            self.btn_refrescar.setEnabled(True)

    def _cargar_tabla(self, usuarios: list[dict]) -> None:
        self.tabla_usuarios.setRowCount(len(usuarios))
        for row, usuario in enumerate(usuarios):
            self._set_cell(
                row,
                0,
                str(usuario.get("id", "")),
                align=Qt.AlignCenter,
                color="#52616B",
                weight=600,
            )
            self._set_cell(row, 1, str(usuario.get("rut", "")))
            self._set_cell(row, 2, str(usuario.get("full_name", "")))
            self._set_cell(row, 3, str(usuario.get("email", "")))
            self._set_cell(
                row,
                4,
                self._nombre_rol(usuario.get("role")),
                align=Qt.AlignCenter,
                weight=600,
            )
            self.tabla_usuarios.setRowHeight(row, 38)

    def _set_cell(
        self,
        row: int,
        col: int,
        texto: str,
        align=Qt.AlignLeft | Qt.AlignVCenter,
        color: str | None = None,
        weight: int = 400,
    ) -> None:
        item = QTableWidgetItem(texto)
        item.setTextAlignment(align)
        if color:
            item.setForeground(QColor(color))
        font = QFont()
        if weight >= 700:
            font.setWeight(QFont.Weight.Bold)
        elif weight >= 600:
            font.setWeight(QFont.Weight.DemiBold)
        else:
            font.setWeight(QFont.Weight.Normal)
        item.setFont(font)
        self.tabla_usuarios.setItem(row, col, item)

    def _nombre_rol(self, role: object) -> str:
        texto = str(role or "").strip()
        if texto.lower() == "admin":
            return "Administrador"
        if texto.lower() == "vecino":
            return "Vecino"
        return texto

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
                rut = creado.get("rut", self.input_rut.text().strip()) if creado else self.input_rut.text().strip()
                rol_id = int(self.cb_rol.currentData())
                rol_texto = "Administrador" if rol_id == 1 else "Vecino"
                QMessageBox.information(
                    self,
                    "Usuario creado",
                    f"Usuario creado correctamente.\n\n"
                    f"Nombre: {nombre}\n"
                    f"RUT: {rut}\n"
                    f"Rol: {rol_texto}",
                )
                self.limpiar()
                self.refrescar()
            else:
                QMessageBox.warning(self, "No fue posible crear el usuario", msg)
        finally:
            self.btn_guardar.setEnabled(True)
            self.btn_guardar.setText("Guardar usuario")
