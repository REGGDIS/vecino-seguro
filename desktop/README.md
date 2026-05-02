# Aplicación desktop VecinoSeguro

Prototipo de la aplicación de escritorio en Python sobre PySide6. La arquitectura
mantiene una separación clara entre vistas, controladores, servicios y
repositorios, lo que permite migrar a Tkinter conservando la lógica de negocio
o reemplazar los repositorios mock por consumo del backend FastAPI.

## Instalación

```bash
cd desktop
python -m venv .venv
source .venv/bin/activate    # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución

```bash
python src/main/main.py
```

## Cuentas de prueba

| Rol           | RUT             | Contraseña |
|---------------|-----------------|------------|
| Vecino        | 12.345.678-5    | Vecino123  |
| Administrador | 11.111.111-1    | Admin123   |
| Vecino        | 22.222.222-2    | Vecino123  |
| Vecino        | 16.828.693-2    | Vecino123  |

## Funcionalidades implementadas

- Login con validación de RUT (algoritmo módulo 11) y contraseña con hash + sal.
- Dashboard con KPIs en vivo (pendientes, en revisión, atendidos, resueltos)
  y reportes recientes.
- Listado de reportes con filtro por estado y panel de detalle integrado.
- Cambio de estado y observaciones disponibles solo para administrador.
- Formulario de registro de emergencia con validaciones de negocio.
- Identidad visual coherente con la paleta verde-azul del logo, badges por
  estado y nivel de urgencia, hoja de estilos QSS centralizada.

## Organización del código

```
desktop/
├── requirements.txt
├── README.md
└── src/
    ├── main/
    │   └── main.py                 # Punto de entrada y contenedor DI
    ├── assets/
    │   ├── logo.svg
    │   └── app.qss                 # Hoja de estilos global
    ├── config/
    │   └── settings.py             # Lectura de variables de entorno
    ├── core/
    │   ├── constants.py
    │   ├── rut_validator.py        # Algoritmo módulo 11
    │   └── password_service.py     # Hash + criterios de seguridad
    ├── models/
    │   └── entities.py             # Usuario, Emergencia y enums
    ├── repositories/
    │   ├── user_repository.py      # Mock en memoria
    │   └── emergency_repository.py # Mock en memoria con datos seed
    ├── services/
    │   └── api_client.py           # Cliente HTTP para el backend FastAPI
    ├── controllers/
    │   ├── auth_controller.py      # Coordina login y sesión
    │   └── emergency_controller.py # Lógica de negocio de reportes
    └── views/
        ├── ui_helpers.py           # Helpers para botones estilizados
        ├── login_view.py
        ├── dashboard_view.py
        ├── emergency_form_view.py
        ├── emergency_list_view.py
        └── main_window.py          # Shell con sidebar y stack
```

## Aplicación de principios SOLID

| Principio | Aplicación |
|-----------|------------|
| **S**ingle Responsibility | `RutValidator` solo valida RUT. `PasswordService` solo gestiona contraseñas. Cada vista solo presenta. |
| **O**pen/Closed           | Nuevos `TipoEmergencia` o `EstadoEmergencia` se agregan extendiendo enums sin tocar código existente. |
| **L**iskov Substitution   | Cualquier implementación que cumpla la interfaz de `EmergencyRepository` (memoria, MySQL, mock para tests) es intercambiable. |
| **I**nterface Segregation | Las vistas reciben solo el controlador que necesitan (`LoginView` recibe `AuthController`; `DashboardView` recibe `EmergencyController`). |
| **D**ependency Inversion  | `main.py` instancia los repositorios y los inyecta en los controladores; los controladores se inyectan en las vistas. Ningún módulo de alto nivel crea sus dependencias. |

## Próximos pasos

- Conectar `AuthController` con el backend FastAPI vía `ApiClient`.
- Reemplazar repositorios mock por implementaciones que consuman la API real.
- Refinar las vistas tras el feedback del equipo.
