"""Modelos del dominio para la app desktop de VecinoSeguro.

Las entidades reflejan los conceptos centrales del sistema: usuarios, roles,
y reportes de emergencia con sus tipos, niveles de urgencia y estados.

Se utilizan dataclasses para mantener los modelos simples, serializables
y fáciles de mapear a/desde JSON cuando el backend FastAPI esté disponible.
"""

from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum


class Rol(str, Enum):
    VECINO = "vecino"
    ADMIN = "admin"


class TipoEmergencia(str, Enum):
    CORTE_LUZ = "Corte de luz"
    ACCIDENTE = "Accidente"
    INCENDIO = "Incendio"
    ROBO = "Robo"
    PERSONA_EXTRAVIADA = "Persona extraviada"
    EMERGENCIA_MEDICA = "Emergencia médica"
    SOLICITUD_AYUDA = "Solicitud de ayuda"
    OTRO = "Otro"


class NivelUrgencia(str, Enum):
    BAJA = "Baja"
    MEDIA = "Media"
    ALTA = "Alta"
    CRITICA = "Crítica"


class EstadoEmergencia(str, Enum):
    PENDIENTE = "Pendiente"
    EN_REVISION = "En revisión"
    ATENDIDO = "Atendido"
    RESUELTO = "Resuelto"


@dataclass
class Usuario:
    rut: str
    nombre: str
    rol: Rol
    password_hash: str
    direccion: str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        d["rol"] = self.rol.value
        return d


@dataclass
class Emergencia:
    id: int
    tipo: TipoEmergencia
    descripcion: str
    ubicacion: str
    nivel_urgencia: NivelUrgencia
    estado: EstadoEmergencia
    rut_reportante: str
    nombre_reportante: str
    fecha_reporte: datetime = field(default_factory=datetime.now)
    observaciones: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "tipo": self.tipo.value,
            "descripcion": self.descripcion,
            "ubicacion": self.ubicacion,
            "nivel_urgencia": self.nivel_urgencia.value,
            "estado": self.estado.value,
            "rut_reportante": self.rut_reportante,
            "nombre_reportante": self.nombre_reportante,
            "fecha_reporte": self.fecha_reporte.isoformat(),
            "observaciones": self.observaciones,
        }
