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
from src.models.entities import Usuario
from src.widgets.buttons import estilizar_boton


class UserFormView(QWidget):
    """Formulario básico para crear vecinos o administradores."""

    def __init__(self, controller: UserController | None = None) -> None:
        super().__init__()
        self._controller = controller or UserController()
        self._usuarios: list[dict] = []
        self._usuario_editando_id: int | None = None
        self._usuario_editando_activo = True
        self._usuario_actual: Usuario | None = None
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
        self.tabla_usuarios.setColumnCount(6)
        self.tabla_usuarios.setHorizontalHeaderLabels(
            ["ID", "RUT", "Nombre", "Email", "Rol", "Estado"]
        )
        self.tabla_usuarios.verticalHeader().setVisible(False)
        self.tabla_usuarios.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_usuarios.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla_usuarios.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_usuarios.setAlternatingRowColors(False)
        self.tabla_usuarios.itemSelectionChanged.connect(self._on_usuario_seleccionado)
        header = self.tabla_usuarios.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.tabla_usuarios.setMinimumHeight(240)
        table_card_lay.addWidget(self.tabla_usuarios)
        outer.addWidget(table_card)

        edit_card = QFrame()
        edit_card.setObjectName("card")
        edit_lay = QVBoxLayout(edit_card)
        edit_lay.setContentsMargins(24, 22, 24, 24)
        edit_lay.setSpacing(14)

        edit_title = QLabel("Editar usuario seleccionado")
        edit_title.setObjectName("h1")
        edit_lay.addWidget(edit_title)

        self.lbl_estado_edicion = QLabel(
            "Selecciona un usuario del listado para editar sus datos."
        )
        self.lbl_estado_edicion.setWordWrap(True)
        self.lbl_estado_edicion.setStyleSheet("color: #52616B; font-size: 12px;")
        edit_lay.addWidget(self.lbl_estado_edicion)

        referencia = QHBoxLayout()
        referencia.setSpacing(20)
        col_id = QVBoxLayout()
        col_id.setSpacing(6)
        col_id.addWidget(self._lbl("ID"))
        self.lbl_edit_id = QLabel("—")
        self.lbl_edit_id.setStyleSheet("color: #102A43; font-size: 13px;")
        col_id.addWidget(self.lbl_edit_id)
        referencia.addLayout(col_id, 1)

        col_rut = QVBoxLayout()
        col_rut.setSpacing(6)
        col_rut.addWidget(self._lbl("RUT"))
        self.lbl_edit_rut = QLabel("—")
        self.lbl_edit_rut.setStyleSheet("color: #102A43; font-size: 13px;")
        col_rut.addWidget(self.lbl_edit_rut)
        referencia.addLayout(col_rut, 3)
        edit_lay.addLayout(referencia)

        campo_edit_nombre = QVBoxLayout()
        campo_edit_nombre.setSpacing(8)
        campo_edit_nombre.addWidget(self._lbl("Nombre completo *"))
        self.input_edit_nombre = QLineEdit()
        self.input_edit_nombre.setMinimumHeight(36)
        self.input_edit_nombre.setPlaceholderText("Nombre completo")
        campo_edit_nombre.addWidget(self.input_edit_nombre)
        edit_lay.addLayout(campo_edit_nombre)

        campo_edit_email = QVBoxLayout()
        campo_edit_email.setSpacing(8)
        campo_edit_email.addWidget(self._lbl("Email *"))
        self.input_edit_email = QLineEdit()
        self.input_edit_email.setMinimumHeight(36)
        self.input_edit_email.setPlaceholderText("correo@vecinoseguro.cl")
        campo_edit_email.addWidget(self.input_edit_email)
        edit_lay.addLayout(campo_edit_email)

        campo_edit_rol = QVBoxLayout()
        campo_edit_rol.setSpacing(8)
        campo_edit_rol.addWidget(self._lbl("Rol *"))
        self.cb_edit_rol = QComboBox()
        self.cb_edit_rol.addItem("Vecino", 2)
        self.cb_edit_rol.addItem("Administrador", 1)
        self.cb_edit_rol.setMinimumHeight(36)
        campo_edit_rol.addWidget(self.cb_edit_rol)
        edit_lay.addLayout(campo_edit_rol)

        estado_row = QHBoxLayout()
        estado_row.setSpacing(10)
        estado_row.addWidget(self._lbl("Estado actual"))
        self.lbl_edit_estado = QLabel("—")
        self.lbl_edit_estado.setStyleSheet("color: #52616B; font-size: 13px;")
        estado_row.addWidget(self.lbl_edit_estado)
        estado_row.addStretch()
        edit_lay.addLayout(estado_row)

        edit_buttons = QHBoxLayout()
        edit_buttons.addStretch()
        self.btn_estado_usuario = QPushButton("Desactivar usuario")
        estilizar_boton(self.btn_estado_usuario, "danger")
        self.btn_estado_usuario.clicked.connect(self._cambiar_estado_usuario)
        edit_buttons.addWidget(self.btn_estado_usuario)

        self.btn_cancelar_edicion = QPushButton("Cancelar edición")
        estilizar_boton(self.btn_cancelar_edicion, "secondary")
        self.btn_cancelar_edicion.clicked.connect(self._cancelar_edicion)
        edit_buttons.addWidget(self.btn_cancelar_edicion)

        self.btn_guardar_edicion = QPushButton("Guardar cambios")
        estilizar_boton(self.btn_guardar_edicion, "primary")
        self.btn_guardar_edicion.clicked.connect(self._guardar_edicion)
        edit_buttons.addWidget(self.btn_guardar_edicion)
        edit_lay.addLayout(edit_buttons)

        outer.addWidget(edit_card)
        self._set_edicion_habilitada(False)
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

    def set_usuario(self, usuario: Usuario) -> None:
        """Recibe el usuario autenticado para evitar autodesactivación."""
        self._usuario_actual = usuario

    def refrescar(self, seleccionar_usuario_id: int | None = None) -> None:
        self.btn_refrescar.setEnabled(False)
        self.lbl_estado_listado.setText("Cargando usuarios registrados...")
        usuario_a_seleccionar = (
            seleccionar_usuario_id
            if seleccionar_usuario_id is not None
            else self._usuario_editando_id
        )
        try:
            ok, msg, usuarios = self._controller.listar_usuarios()
            if not ok:
                self._usuarios = []
                self.tabla_usuarios.setRowCount(0)
                self.lbl_estado_listado.setText(msg)
                self._limpiar_edicion()
                return

            self._cargar_tabla(usuarios)
            if usuarios:
                self.lbl_estado_listado.setText(
                    f"{len(usuarios)} usuario(s) registrado(s)."
                )
                if usuario_a_seleccionar is not None:
                    if not self._seleccionar_usuario_por_id(usuario_a_seleccionar):
                        self._limpiar_edicion()
            else:
                self.lbl_estado_listado.setText("No hay usuarios registrados.")
                self._limpiar_edicion()
        finally:
            self.btn_refrescar.setEnabled(True)

    def _cargar_tabla(self, usuarios: list[dict]) -> None:
        self._usuarios = usuarios
        senales_bloqueadas = self.tabla_usuarios.blockSignals(True)
        self.tabla_usuarios.setRowCount(len(usuarios))
        for row, usuario in enumerate(usuarios):
            self._set_cell(
                row,
                0,
                str(usuario.get("id", "")),
                align=Qt.AlignCenter,
                color="#52616B",
                weight=600,
                data=usuario,
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
            activo = self._usuario_activo(usuario)
            self._set_cell(
                row,
                5,
                "Activo" if activo else "Inactivo",
                align=Qt.AlignCenter,
                color="#16812C" if activo else "#D92D20",
                weight=600,
            )
            self.tabla_usuarios.setRowHeight(row, 38)
        self.tabla_usuarios.blockSignals(senales_bloqueadas)

    def _set_cell(
        self,
        row: int,
        col: int,
        texto: str,
        align=Qt.AlignLeft | Qt.AlignVCenter,
        color: str | None = None,
        weight: int = 400,
        data: object | None = None,
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
        if data is not None:
            item.setData(Qt.UserRole, data)
        self.tabla_usuarios.setItem(row, col, item)

    def _nombre_rol(self, role: object) -> str:
        texto = str(role or "").strip()
        if texto.lower() == "admin":
            return "Administrador"
        if texto.lower() == "vecino":
            return "Vecino"
        return texto

    def _on_usuario_seleccionado(self) -> None:
        rows = self.tabla_usuarios.selectionModel().selectedRows()
        if not rows:
            self._limpiar_edicion()
            return

        usuario = self._usuario_desde_fila(rows[0].row())
        if usuario is None:
            self._limpiar_edicion()
            return
        self._cargar_edicion(usuario)

    def _usuario_desde_fila(self, row: int) -> dict | None:
        item = self.tabla_usuarios.item(row, 0)
        if item is None:
            return None
        usuario = item.data(Qt.UserRole)
        return usuario if isinstance(usuario, dict) else None

    def _cargar_edicion(self, usuario: dict) -> None:
        user_id = self._int_or_none(usuario.get("id"))
        if user_id is None:
            self._limpiar_edicion()
            return

        self._usuario_editando_id = user_id
        self.lbl_edit_id.setText(str(user_id))
        self.lbl_edit_rut.setText(str(usuario.get("rut", "")))
        self.input_edit_nombre.setText(str(usuario.get("full_name", "")))
        self.input_edit_email.setText(str(usuario.get("email", "")))

        role_id = self._int_or_none(usuario.get("role_id")) or 2
        idx = self.cb_edit_rol.findData(role_id)
        self.cb_edit_rol.setCurrentIndex(idx if idx >= 0 else 0)

        self.lbl_estado_edicion.setText(
            "Puedes editar nombre completo, email y rol. El ID y RUT son solo referencia."
        )
        self._usuario_editando_activo = self._usuario_activo(usuario)
        self._set_edicion_habilitada(True)
        self._actualizar_estado_edicion()

    def _limpiar_edicion(self) -> None:
        self._usuario_editando_id = None
        self._usuario_editando_activo = True
        self.lbl_edit_id.setText("—")
        self.lbl_edit_rut.setText("—")
        self.lbl_edit_estado.setText("—")
        self.input_edit_nombre.clear()
        self.input_edit_email.clear()
        self.cb_edit_rol.setCurrentIndex(0)
        self.lbl_estado_edicion.setText(
            "Selecciona un usuario del listado para editar sus datos."
        )
        self._set_edicion_habilitada(False)

    def _set_edicion_habilitada(self, habilitada: bool) -> None:
        self.input_edit_nombre.setEnabled(habilitada)
        self.input_edit_email.setEnabled(habilitada)
        self.cb_edit_rol.setEnabled(habilitada)
        self.btn_guardar_edicion.setEnabled(habilitada)
        self.btn_cancelar_edicion.setEnabled(habilitada)
        if not habilitada:
            self.btn_estado_usuario.setEnabled(False)

    def _cancelar_edicion(self) -> None:
        senales_bloqueadas = self.tabla_usuarios.blockSignals(True)
        self.tabla_usuarios.clearSelection()
        self.tabla_usuarios.blockSignals(senales_bloqueadas)
        self._limpiar_edicion()

    def _guardar_edicion(self) -> None:
        if self._usuario_editando_id is None:
            QMessageBox.warning(
                self,
                "Sin usuario seleccionado",
                "Selecciona un usuario del listado antes de guardar cambios.",
            )
            return

        user_id = self._usuario_editando_id
        self.btn_guardar_edicion.setEnabled(False)
        self.btn_guardar_edicion.setText("Guardando...")
        try:
            ok, msg, actualizado = self._controller.editar_usuario(
                user_id=user_id,
                full_name=self.input_edit_nombre.text(),
                email=self.input_edit_email.text(),
                role_id=int(self.cb_edit_rol.currentData()),
            )
            if not ok:
                QMessageBox.warning(self, "No fue posible editar el usuario", msg)
                return

            nombre = (
                actualizado.get("full_name", self.input_edit_nombre.text().strip())
                if actualizado
                else self.input_edit_nombre.text().strip()
            )
            QMessageBox.information(
                self,
                "Usuario actualizado",
                f"Usuario actualizado correctamente.\n\nNombre: {nombre}",
            )
            self.refrescar(seleccionar_usuario_id=user_id)
        finally:
            self.btn_guardar_edicion.setText("Guardar cambios")
            self.btn_guardar_edicion.setEnabled(self._usuario_editando_id is not None)

    def _cambiar_estado_usuario(self) -> None:
        if self._usuario_editando_id is None:
            return

        if self._es_usuario_actual() and self._usuario_editando_activo:
            QMessageBox.warning(
                self,
                "Acción no permitida",
                "No puedes desactivar tu propia cuenta mientras estás en sesión.",
            )
            return

        activar = not self._usuario_editando_activo
        if activar:
            titulo = "Activar usuario"
            mensaje = (
                "¿Activar este usuario?\n\n"
                "El usuario podrá iniciar sesión nuevamente con sus credenciales."
            )
        else:
            titulo = "Desactivar usuario"
            mensaje = (
                "¿Desactivar este usuario?\n\n"
                "El usuario no podrá iniciar sesión, pero sus reportes e historial "
                "se conservarán."
            )

        respuesta = QMessageBox.question(
            self,
            titulo,
            mensaje,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if respuesta != QMessageBox.StandardButton.Yes:
            return

        user_id = self._usuario_editando_id
        self.btn_estado_usuario.setEnabled(False)
        self.btn_estado_usuario.setText("Actualizando...")
        try:
            ok, msg, actualizado = self._controller.cambiar_estado_usuario(
                user_id,
                activar,
            )
            if not ok:
                QMessageBox.warning(self, "No fue posible cambiar el estado", msg)
                return

            QMessageBox.information(self, "Estado actualizado", msg)
            self.refrescar(seleccionar_usuario_id=user_id)
            if actualizado:
                self._cargar_edicion(actualizado)
        finally:
            self._actualizar_estado_edicion()

    def _seleccionar_usuario_por_id(self, user_id: int) -> bool:
        for row in range(self.tabla_usuarios.rowCount()):
            usuario = self._usuario_desde_fila(row)
            if usuario and self._int_or_none(usuario.get("id")) == user_id:
                self.tabla_usuarios.selectRow(row)
                return True
        return False

    def _int_or_none(self, value: object) -> int | None:
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    def _usuario_activo(self, usuario: dict) -> bool:
        return bool(usuario.get("is_active", True))

    def _actualizar_estado_edicion(self) -> None:
        if self._usuario_editando_id is None:
            self.lbl_edit_estado.setText("—")
            self.btn_estado_usuario.setText("Desactivar usuario")
            self.btn_estado_usuario.setEnabled(False)
            return

        if self._usuario_editando_activo:
            self.lbl_edit_estado.setText("Activo")
            self.lbl_edit_estado.setStyleSheet("color: #16812C; font-size: 13px;")
            self.btn_estado_usuario.setText("Desactivar usuario")
            estilizar_boton(self.btn_estado_usuario, "danger")
            self.btn_estado_usuario.setEnabled(not self._es_usuario_actual())
            if self._es_usuario_actual():
                self.btn_estado_usuario.setToolTip(
                    "No puedes desactivar tu propia cuenta mientras estás en sesión."
                )
            else:
                self.btn_estado_usuario.setToolTip("")
        else:
            self.lbl_edit_estado.setText("Inactivo")
            self.lbl_edit_estado.setStyleSheet("color: #D92D20; font-size: 13px;")
            self.btn_estado_usuario.setText("Activar usuario")
            estilizar_boton(self.btn_estado_usuario, "success")
            self.btn_estado_usuario.setEnabled(True)
            self.btn_estado_usuario.setToolTip("")

    def _es_usuario_actual(self) -> bool:
        if self._usuario_actual is None or self._usuario_actual.id is None:
            return False
        return self._usuario_editando_id == self._usuario_actual.id

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
