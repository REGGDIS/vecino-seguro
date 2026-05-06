"""Repositorio de usuarios en memoria.

Implementación mock para el prototipo. Cumple un contrato simple
(`find_by_rut`, `save`, `list_all`) que cuando el backend FastAPI esté
disponible, se reemplazará por una implementación que use `ApiClient`,
sin necesidad de modificar los controladores ni las vistas
(Principio de Inversión de Dependencias).
"""

from typing import Optional

from src.core.password_service import PasswordService
from src.core.rut_validator import RutValidator
from src.models.entities import Rol, Usuario


class UserRepository:
    """Persistencia en memoria de usuarios para el prototipo."""

    def __init__(self) -> None:
        self._usuarios: dict[str, Usuario] = {}
        self._seed()

    def _seed(self) -> None:
        """Carga los usuarios de demostración usados en las pruebas locales."""
        seed_data = [
            ("12345678-5", "Franco Quezada", Rol.VECINO, "Vecino123",
             "Av. Los Carrera 1234, Los Ángeles"),
            ("11111111-1", "Roberto González", Rol.ADMIN, "Admin123",
             "Calle Lautaro 456, Los Ángeles"),
            ("22222222-2", "Raymond Civil", Rol.VECINO, "Vecino123",
             "Pasaje Las Camelias 789, Los Ángeles"),
            ("16828693-2", "María Pérez", Rol.VECINO, "Vecino123",
             "Av. Alemania 321, Los Ángeles"),
        ]
        for rut, nombre, rol, password, direccion in seed_data:
            rut_formateado = RutValidator.formatear(rut)
            self._usuarios[rut_formateado] = Usuario(
                rut=rut_formateado,
                nombre=nombre,
                rol=rol,
                password_hash=PasswordService.hash_password(password),
                direccion=direccion,
            )

    def find_by_rut(self, rut: str) -> Optional[Usuario]:
        return self._usuarios.get(rut)

    def save(self, usuario: Usuario) -> Usuario:
        self._usuarios[usuario.rut] = usuario
        return usuario

    def list_all(self) -> list[Usuario]:
        return list(self._usuarios.values())
