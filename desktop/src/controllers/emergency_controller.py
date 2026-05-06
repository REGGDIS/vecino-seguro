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
    TipoEmergencia,
    Usuario,
)
from src.repositories.emergency_repository import EmergencyRepository
from src.services.api_client import ApiClient


class EmergencyController:
    """Coordina formularios y servicios relacionados con emergencias."""

    def __init__(
        self,
        repository: EmergencyRepository | None = None,
        api_client: ApiClient | None = None,
    ) -> None:
        self._repo = repository or EmergencyRepository()
        self._api = api_client

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
            tipo=TipoEmergencia(payload["tipo"]),
            descripcion=payload["descripcion"],
            ubicacion=payload["ubicacion"],
            nivel_urgencia=NivelUrgencia(payload["nivel_urgencia"]),
            estado=EstadoEmergencia.PENDIENTE,
            rut_reportante=payload["rut_reportante"],
            nombre_reportante=payload["nombre_reportante"],
            fecha_reporte=datetime.now(),
        )
        return self._repo.save(nueva).to_dict()

    # ------------------------------------------------------------------
    # API extendida para uso desde las vistas
    # ------------------------------------------------------------------
    def listar(self) -> list[Emergencia]:
        return self._repo.list_all()

    def listar_por_estado(self, estado: EstadoEmergencia) -> list[Emergencia]:
        return self._repo.filter_by_estado(estado)

    def listar_de_usuario(self, rut: str) -> list[Emergencia]:
        return [e for e in self._repo.list_all() if e.rut_reportante == rut]

    def obtener(self, emergencia_id: int) -> Optional[Emergencia]:
        return self._repo.find_by_id(emergencia_id)

    def estadisticas(self) -> dict[EstadoEmergencia, int]:
        return self._repo.count_by_estado()

    def registrar(
        self,
        usuario: Usuario,
        tipo: TipoEmergencia,
        descripcion: str,
        ubicacion: str,
        nivel_urgencia: NivelUrgencia,
    ) -> tuple[bool, str, Optional[Emergencia]]:
        """Valida los datos del reporte y lo persiste en estado Pendiente."""
        if not descripcion.strip():
            return False, "La descripción no puede estar vacía.", None
        if len(descripcion.strip()) < 10:
            return False, "La descripción debe tener al menos 10 caracteres.", None
        if not ubicacion.strip():
            return False, "Debe indicar una ubicación.", None

        nueva = Emergencia(
            id=0,
            tipo=tipo,
            descripcion=descripcion.strip(),
            ubicacion=ubicacion.strip(),
            nivel_urgencia=nivel_urgencia,
            estado=EstadoEmergencia.PENDIENTE,
            rut_reportante=usuario.rut,
            nombre_reportante=usuario.nombre,
            fecha_reporte=datetime.now(),
        )
        guardada = self._repo.save(nueva)
        return True, f"Emergencia #{guardada.id} registrada.", guardada

    def cambiar_estado(
        self,
        emergencia_id: int,
        nuevo_estado: EstadoEmergencia,
        observaciones: str = "",
    ) -> tuple[bool, str]:
        emergencia = self._repo.find_by_id(emergencia_id)
        if not emergencia:
            return False, "Emergencia no encontrada."
        emergencia.estado = nuevo_estado
        if observaciones:
            emergencia.observaciones = observaciones
        self._repo.save(emergencia)
        return True, f"Estado actualizado a '{nuevo_estado.value}'."
