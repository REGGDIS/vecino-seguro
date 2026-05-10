"""Modelos del dominio para la app desktop de VecinoSeguro.

Las entidades reflejan los conceptos centrales del sistema: usuarios, roles,
y reportes de emergencia con sus tipos, niveles de urgencia y estados.

Se utilizan dataclasses para mantener los modelos simples, serializables
y fáciles de mapear a/desde JSON cuando el backend FastAPI esté disponible.
"""

import unicodedata
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from typing import TypeVar


EnumT = TypeVar("EnumT", bound=Enum)


def normalizar_texto(valor: str) -> str:
    """Normaliza texto para comparar enums con o sin tildes, espacios o guiones."""
    texto = valor.strip().replace("_", " ").lower()
    texto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def normalizar_enum(valor: EnumT | str, enum_cls: type[EnumT], campo: str) -> EnumT:
    """Convierte strings válidos al enum esperado y rechaza valores inválidos."""
    if isinstance(valor, enum_cls):
        return valor
    if isinstance(valor, str):
        texto = normalizar_texto(valor)
        for miembro in enum_cls:
            if texto in (
                normalizar_texto(miembro.value),
                normalizar_texto(miembro.name),
            ):
                return miembro
    raise ValueError(f"{campo} inválido: {valor!r}")


class Rol(str, Enum):
    VECINO = "vecino"
    ADMIN = "admin"


class TipoEmergencia(str, Enum):
    CORTE_LUZ = "Corte de luz"
    ACCIDENTE = "Accidente"
    INCENDIO = "Incendio"
    ROBO = "Robo"
    ROBO_EN_PROCESO = "Robo en proceso"
    INUNDACION_MENOR = "Inundación menor"
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

    def __post_init__(self) -> None:
        self.normalizar_campos()

    def normalizar_campos(self) -> None:
        """Asegura que el rol se mantenga como enum."""
        self.rol = normalizar_enum(self.rol, Rol, "rol")

    def to_dict(self) -> dict:
        self.normalizar_campos()
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

    def __post_init__(self) -> None:
        self.normalizar_campos()

    def normalizar_campos(self) -> None:
        """Asegura que los campos categóricos se mantengan como enums."""
        self.tipo = normalizar_enum(self.tipo, TipoEmergencia, "tipo")
        self.nivel_urgencia = normalizar_enum(
            self.nivel_urgencia, NivelUrgencia, "nivel_urgencia"
        )
        self.estado = normalizar_enum(self.estado, EstadoEmergencia, "estado")

    def to_dict(self) -> dict:
        self.normalizar_campos()
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
