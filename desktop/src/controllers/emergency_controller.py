"""Controlador de emergencias.

Encapsula la lógica de negocio de los reportes y mantiene la separación
respecto del toolkit visual. Las vistas nunca consultan el repositorio de
forma directa, sino que pasan por este controlador.

Mantiene la API base (`list_emergencies`, `create_emergency`) y agrega los
métodos necesarios para registrar, filtrar, buscar por id y cambiar el
estado de los reportes.
"""

from datetime import datetime
from typing import Optional

from src.models.entities import (
    Emergencia,
    EstadoEmergencia,
    NivelUrgencia,
    Rol,
    TipoEmergencia,
    Usuario,
    normalizar_enum,
)
from src.repositories.emergency_repository import EmergencyRepository
from src.services.api_client import ApiClient, ApiClientError


EMERGENCY_TYPE_OPTIONS = [
    {"value": "robo", "label": "Robo"},
    {"value": "incendio", "label": "Incendio"},
    {"value": "accidente", "label": "Accidente"},
    {"value": "emergencia_medica", "label": "Emergencia médica"},
    {"value": "corte_luz", "label": "Corte de luz"},
    {"value": "persona_extraviada", "label": "Persona extraviada"},
    {"value": "solicitud_ayuda", "label": "Solicitud de ayuda"},
    {"value": "otro", "label": "Otro"},
]

URGENCY_LEVEL_OPTIONS = [
    {"value": "baja", "label": "Baja"},
    {"value": "media", "label": "Media"},
    {"value": "alta", "label": "Alta"},
    {"value": "critica", "label": "Crítica"},
]

STATUS_OPTIONS = [
    {"value": "pendiente", "label": "Pendiente"},
    {"value": "en_revision", "label": "En revisión"},
    {"value": "resuelto", "label": "Resuelto"},
]

BACKEND_TYPE_BY_ENUM = {
    TipoEmergencia.ROBO: "robo",
    TipoEmergencia.INCENDIO: "incendio",
    TipoEmergencia.ACCIDENTE: "accidente",
    TipoEmergencia.EMERGENCIA_MEDICA: "emergencia_medica",
    TipoEmergencia.CORTE_LUZ: "corte_luz",
    TipoEmergencia.PERSONA_EXTRAVIADA: "persona_extraviada",
    TipoEmergencia.SOLICITUD_AYUDA: "solicitud_ayuda",
    TipoEmergencia.OTRO: "otro",
}

BACKEND_URGENCY_BY_ENUM = {
    NivelUrgencia.BAJA: "baja",
    NivelUrgencia.MEDIA: "media",
    NivelUrgencia.ALTA: "alta",
    NivelUrgencia.CRITICA: "critica",
}

BACKEND_STATUS_BY_ENUM = {
    EstadoEmergencia.PENDIENTE: "pendiente",
    EstadoEmergencia.EN_REVISION: "en_revision",
    EstadoEmergencia.RESUELTO: "resuelto",
}

# Mapeo temporal para las cuentas mock del desktop contra seed.sql.
PROTOTYPE_BACKEND_USER_ID_BY_RUT = {
    "11111111-1": 1,
    "22222222-2": 2,
    "13456789-9": 3,
}
PROTOTYPE_DEFAULT_VECINO_USER_ID = 2


class EmergencyController:
    """Coordina formularios y servicios relacionados con emergencias."""

    def __init__(
        self,
        repository: EmergencyRepository | None = None,
        api_client: ApiClient | None = None,
    ) -> None:
        self._repo = repository or EmergencyRepository()
        self._api = api_client
        self.backend_error: str | None = None
        self._ultima_lista: list[Emergencia] = []

    # ------------------------------------------------------------------
    # API base del stub original (firma compatible)
    # ------------------------------------------------------------------
    def list_emergencies(self) -> list[dict]:
        """Devuelve todas las emergencias serializadas a diccionario."""
        return [e.to_dict() for e in self._repo.list_all()]

    def create_emergency(self, payload: dict) -> dict:
        """Crea una emergencia a partir de un payload serializado."""
        nueva = Emergencia(
            id=0,
            tipo=normalizar_enum(payload["tipo"], TipoEmergencia, "tipo"),
            descripcion=payload["descripcion"],
            ubicacion=payload["ubicacion"],
            nivel_urgencia=normalizar_enum(
                payload["nivel_urgencia"], NivelUrgencia, "nivel_urgencia"
            ),
            estado=EstadoEmergencia.PENDIENTE,
            rut_reportante=payload["rut_reportante"],
            nombre_reportante=payload["nombre_reportante"],
            fecha_reporte=datetime.now(),
        )
        return self._repo.save(nueva).to_dict()

    # ------------------------------------------------------------------
    # API extendida para uso desde las vistas
    # ------------------------------------------------------------------
    def obtener_catalogos(self) -> dict:
        """Devuelve catalogos del backend o un fallback local compatible."""
        if self._api is not None:
            try:
                catalogos = self._api.get_emergency_catalogs()
                if self._catalogos_validos(catalogos):
                    return catalogos
            except ApiClientError as exc:
                self.backend_error = exc.message

        return {
            "emergency_types": EMERGENCY_TYPE_OPTIONS,
            "urgency_levels": URGENCY_LEVEL_OPTIONS,
            "statuses": STATUS_OPTIONS,
        }

    def listar(self) -> list[Emergencia]:
        self.backend_error = None

        if self._api is not None:
            datos = self._api.get_emergencies()
            if datos is not None:
                emergencias = self._parsear_emergencias(datos)
                if emergencias or datos == []:
                    self._ultima_lista = emergencias
                    return emergencias

                self.backend_error = (
                    "El backend respondió, pero no se pudieron interpretar "
                    "las emergencias recibidas."
                )
            else:
                self.backend_error = (
                    "No se pudo conectar con el backend. "
                    "Verifica que el servidor esté encendido."
                )

        emergencias_locales = self._repo.list_all()
        self._ultima_lista = emergencias_locales
        return emergencias_locales

    def _parsear_emergencias(self, datos: list[dict]) -> list[Emergencia]:
        """Convierte los dicts del backend en objetos Emergencia."""
        resultado = []
        for d in datos:
            try:
                resultado.append(self._parsear_emergencia_backend(d))
            except Exception:
                continue
        return resultado

    def _parsear_emergencia_backend(
        self,
        dato: dict,
        usuario: Usuario | None = None,
    ) -> Emergencia:
        user_id = dato.get("user_id", "")
        return Emergencia(
            id=dato.get("id", 0),
            tipo=normalizar_enum(dato.get("type", ""), TipoEmergencia, "tipo"),
            descripcion=dato.get("description", ""),
            ubicacion=dato.get("location", ""),
            nivel_urgencia=normalizar_enum(
                dato.get("urgency_level", ""), NivelUrgencia, "nivel_urgencia"
            ),
            estado=normalizar_enum(
                dato.get("status", ""), EstadoEmergencia, "estado"
            ),
            rut_reportante=usuario.rut if usuario else str(user_id),
            nombre_reportante=usuario.nombre if usuario else f"Usuario {user_id}",
            fecha_reporte=self._parsear_fecha(dato.get("created_at")),
        )

    def _parsear_fecha(self, valor: object) -> datetime:
        if isinstance(valor, datetime):
            return valor
        if not valor:
            return datetime.now()
        return datetime.fromisoformat(str(valor).replace("Z", "+00:00"))

    def listar_por_estado(self, estado: EstadoEmergencia) -> list[Emergencia]:
        return [e for e in self.listar() if e.estado == estado]

    def listar_de_usuario(self, rut: str) -> list[Emergencia]:
        return [e for e in self._repo.list_all() if e.rut_reportante == rut]

    def obtener(self, emergencia_id: int) -> Optional[Emergencia]:
        for emergencia in self._ultima_lista:
            if emergencia.id == emergencia_id:
                return emergencia
        return self._repo.find_by_id(emergencia_id)

    def estadisticas(
        self, emergencias: list[Emergencia] | None = None
    ) -> dict[EstadoEmergencia, int]:
        datos = emergencias if emergencias is not None else self.listar()
        return {
            EstadoEmergencia.PENDIENTE: sum(
                1 for e in datos if e.estado == EstadoEmergencia.PENDIENTE
            ),
            EstadoEmergencia.EN_REVISION: sum(
                1 for e in datos if e.estado == EstadoEmergencia.EN_REVISION
            ),
            EstadoEmergencia.ATENDIDO: sum(
                1 for e in datos if e.estado == EstadoEmergencia.ATENDIDO
            ),
            EstadoEmergencia.RESUELTO: sum(
                1 for e in datos if e.estado == EstadoEmergencia.RESUELTO
            ),
        }

    def registrar(
        self,
        usuario: Usuario,
        tipo: TipoEmergencia | str,
        descripcion: str,
        ubicacion: str,
        nivel_urgencia: NivelUrgencia | str,
    ) -> tuple[bool, str, Optional[Emergencia]]:
        """Valida los datos del reporte y lo registra en backend si existe."""
        if usuario is None:
            return False, "Debe iniciar sesión para registrar una emergencia.", None
        if not descripcion.strip():
            return False, "La descripción no puede estar vacía.", None
        if len(descripcion.strip()) < 10:
            return False, "La descripción debe tener al menos 10 caracteres.", None
        if not ubicacion.strip():
            return False, "Debe indicar una ubicación.", None

        try:
            tipo_normalizado = normalizar_enum(tipo, TipoEmergencia, "tipo")
            urgencia_normalizada = normalizar_enum(
                nivel_urgencia, NivelUrgencia, "nivel_urgencia"
            )
            backend_type = self._backend_type(tipo_normalizado)
            backend_urgency = self._backend_urgency(urgencia_normalizada)
        except ValueError:
            return (
                False,
                "El backend rechazó la solicitud. Verifica tipo, urgencia "
                "y campos obligatorios.",
                None,
            )

        user_id = self._backend_user_id(usuario)
        if user_id is None:
            return False, "No se encontró un identificador de usuario válido.", None

        if self._api is not None:
            payload = {
                "user_id": user_id,
                "type": backend_type,
                "description": descripcion.strip(),
                "location": ubicacion.strip(),
                "urgency_level": backend_urgency,
            }
            try:
                creada = self._api.create_emergency(payload)
                emergencia = self._parsear_emergencia_backend(creada, usuario)
                return True, f"Emergencia #{emergencia.id} registrada.", emergencia
            except ApiClientError as exc:
                return False, exc.message, None
            except Exception:
                return (
                    False,
                    "La emergencia fue creada, pero no se pudo interpretar "
                    "la respuesta del backend.",
                    None,
                )

        nueva = Emergencia(
            id=0,
            tipo=tipo_normalizado,
            descripcion=descripcion.strip(),
            ubicacion=ubicacion.strip(),
            nivel_urgencia=urgencia_normalizada,
            estado=EstadoEmergencia.PENDIENTE,
            rut_reportante=usuario.rut,
            nombre_reportante=usuario.nombre,
            fecha_reporte=datetime.now(),
        )
        guardada = self._repo.save(nueva)
        return True, f"Emergencia #{guardada.id} registrada.", guardada

    def _catalogos_validos(self, catalogos: object) -> bool:
        if not isinstance(catalogos, dict):
            return False
        for clave in ("emergency_types", "urgency_levels", "statuses"):
            opciones = catalogos.get(clave)
            if not isinstance(opciones, list):
                return False
            if not all(
                isinstance(op, dict) and op.get("value") and op.get("label")
                for op in opciones
            ):
                return False
        return True

    def _backend_type(self, tipo: TipoEmergencia) -> str:
        if tipo not in BACKEND_TYPE_BY_ENUM:
            raise ValueError(f"tipo no soportado por backend: {tipo.value}")
        return BACKEND_TYPE_BY_ENUM[tipo]

    def _backend_urgency(self, urgencia: NivelUrgencia) -> str:
        return BACKEND_URGENCY_BY_ENUM[urgencia]

    def _backend_status(self, estado: EstadoEmergencia) -> str:
        if estado not in BACKEND_STATUS_BY_ENUM:
            raise ValueError(f"estado no soportado por backend: {estado.value}")
        return BACKEND_STATUS_BY_ENUM[estado]

    def _backend_user_id(self, usuario: Usuario) -> int | None:
        user_id = getattr(usuario, "id", None)
        if isinstance(user_id, int) and user_id > 0:
            return user_id

        rut_normalizado = usuario.rut.replace(".", "")
        if rut_normalizado in PROTOTYPE_BACKEND_USER_ID_BY_RUT:
            return PROTOTYPE_BACKEND_USER_ID_BY_RUT[rut_normalizado]

        if usuario.rol == Rol.VECINO:
            return PROTOTYPE_DEFAULT_VECINO_USER_ID

        return None

    def _actualizar_cache(self, emergencia_actualizada: Emergencia) -> None:
        for index, emergencia in enumerate(self._ultima_lista):
            if emergencia.id == emergencia_actualizada.id:
                self._ultima_lista[index] = emergencia_actualizada
                return
        self._ultima_lista.append(emergencia_actualizada)

    def _mensaje_api_error(self, exc: ApiClientError) -> str:
        if isinstance(exc.detail, str) and exc.detail:
            return exc.detail
        if exc.status_code == 404:
            return "Emergencia no encontrada en el backend."
        return exc.message

    def cambiar_estado(
        self,
        emergencia_id: int,
        nuevo_estado: EstadoEmergencia | str,
        observaciones: str = "",
    ) -> tuple[bool, str]:
        if nuevo_estado is None:
            return False, "Debe seleccionar un estado."

        try:
            estado_normalizado = normalizar_enum(
                nuevo_estado, EstadoEmergencia, "estado"
            )
        except ValueError:
            return False, "El estado seleccionado no es válido."

        if self._api is not None:
            if estado_normalizado == EstadoEmergencia.ATENDIDO:
                return (
                    False,
                    'El estado "Atendido" aún no está disponible en el backend.',
                )

            try:
                backend_status = self._backend_status(estado_normalizado)
                payload = {"status": backend_status}
                if observaciones:
                    payload["comment"] = observaciones

                actualizada = self._api.update_emergency_status(
                    emergencia_id,
                    payload,
                )
                emergencia = self._parsear_emergencia_backend(actualizada)
                self._actualizar_cache(emergencia)
                return True, f"Estado actualizado a '{estado_normalizado.value}'."
            except ApiClientError as exc:
                return False, self._mensaje_api_error(exc)
            except Exception:
                return (
                    False,
                    "El backend respondió, pero no se pudo interpretar "
                    "la emergencia actualizada.",
                )

        emergencia = self._repo.find_by_id(emergencia_id)
        if not emergencia:
            return False, "Emergencia no encontrada."
        emergencia.estado = estado_normalizado
        if observaciones:
            emergencia.observaciones = observaciones
        self._repo.save(emergencia)
        self._actualizar_cache(emergencia)
        return True, f"Estado actualizado a '{estado_normalizado.value}'."
