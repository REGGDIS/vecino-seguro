"""Repositorio de emergencias en memoria.

Mock para el prototipo desktop. Cuando el backend FastAPI esté operativo,
una implementación alterna utilizará `ApiClient` cumpliendo la misma
interfaz pública.
"""

from datetime import datetime, timedelta
from typing import Optional

from src.core.rut_validator import RutValidator
from src.models.entities import (
    Emergencia,
    EstadoEmergencia,
    NivelUrgencia,
    TipoEmergencia,
)


class EmergencyRepository:
    """Persistencia en memoria de reportes de emergencia."""

    def __init__(self) -> None:
        self._emergencias: list[Emergencia] = []
        self._next_id = 1
        self._seed()

    def _seed(self) -> None:
        ahora = datetime.now()
        # Datos de demostración representativos del dominio
        seed = [
            (TipoEmergencia.CORTE_LUZ,
             "Sin luz desde hace 2 horas en toda la cuadra.",
             "Av. Los Carrera con Lautaro",
             NivelUrgencia.MEDIA, EstadoEmergencia.EN_REVISION,
             "12345678-5", "Franco Quezada", ahora - timedelta(hours=2)),

            (TipoEmergencia.ROBO,
             "Persona sospechosa intentando abrir vehículos estacionados.",
             "Pasaje Las Camelias 789",
             NivelUrgencia.ALTA, EstadoEmergencia.PENDIENTE,
             "22222222-2", "Raymond Civil", ahora - timedelta(minutes=30)),

            (TipoEmergencia.INCENDIO,
             "Humo saliendo de un patio trasero, posible quema.",
             "Calle Colo Colo 234",
             NivelUrgencia.CRITICA, EstadoEmergencia.ATENDIDO,
             "16828693-2", "María Pérez", ahora - timedelta(hours=5)),

            (TipoEmergencia.PERSONA_EXTRAVIADA,
             "Adulto mayor con Alzheimer salió de casa y no ha vuelto.",
             "Villa Los Aromos, sector norte",
             NivelUrgencia.ALTA, EstadoEmergencia.EN_REVISION,
             "12345678-5", "Franco Quezada", ahora - timedelta(hours=1)),

            (TipoEmergencia.EMERGENCIA_MEDICA,
             "Vecina con malestar, requiere ambulancia.",
             "Av. Alemania 321",
             NivelUrgencia.ALTA, EstadoEmergencia.RESUELTO,
             "16828693-2", "María Pérez", ahora - timedelta(days=1)),

            (TipoEmergencia.SOLICITUD_AYUDA,
             "Se necesita ayuda para mover árbol caído que bloquea calle.",
             "Calle Lautaro 456",
             NivelUrgencia.BAJA, EstadoEmergencia.PENDIENTE,
             "22222222-2", "Raymond Civil", ahora - timedelta(minutes=15)),
        ]
        for (tipo, desc, ubic, urg, est, rut, nom, fecha) in seed:
            self._emergencias.append(Emergencia(
                id=self._next_id,
                tipo=tipo,
                descripcion=desc,
                ubicacion=ubic,
                nivel_urgencia=urg,
                estado=est,
                rut_reportante=RutValidator.formatear(rut),
                nombre_reportante=nom,
                fecha_reporte=fecha,
            ))
            self._next_id += 1

    def list_all(self) -> list[Emergencia]:
        return sorted(self._emergencias,
                      key=lambda e: e.fecha_reporte, reverse=True)

    def find_by_id(self, emergencia_id: int) -> Optional[Emergencia]:
        for e in self._emergencias:
            if e.id == emergencia_id:
                return e
        return None

    def save(self, emergencia: Emergencia) -> Emergencia:
        if emergencia.id == 0:
            emergencia.id = self._next_id
            self._next_id += 1
            self._emergencias.append(emergencia)
        else:
            for i, e in enumerate(self._emergencias):
                if e.id == emergencia.id:
                    self._emergencias[i] = emergencia
                    break
        return emergencia

    def filter_by_estado(self, estado: EstadoEmergencia) -> list[Emergencia]:
        return [e for e in self.list_all() if e.estado == estado]

    def count_by_estado(self) -> dict[EstadoEmergencia, int]:
        contadores = {estado: 0 for estado in EstadoEmergencia}
        for e in self._emergencias:
            contadores[e.estado] += 1
        return contadores
