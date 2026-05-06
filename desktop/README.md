# Aplicación desktop VecinoSeguro

Mockup o prototipo frontend inicial de la aplicación de escritorio de
**VecinoSeguro**, desarrollado con **Python + PySide6** según los
requerimientos de la Issue #2.

> Responsable: **Franco Quezada** — Mockup desktop (PySide6).

## Instalación

```bash
cd desktop
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
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

## Pantallas implementadas

- **Login** con validación de RUT (módulo 11) y mensajes de error claros.
- **Dashboard** con KPIs por estado, accesos rápidos y reportes recientes.
- **Formulario de registro de emergencia** con validaciones de negocio.
- **Listado de emergencias** con filtro por estado y panel de detalle.
- **Detalle del reporte** con cambio de estado disponible solo para administradores.

## Identidad visual

La aplicación sigue la **Guía de Imagen Corporativa UI** de VecinoSeguro
(mayo 2026). Los tokens de color y la tipografía se definen una sola vez
en `src/core/colors.py` y se reutilizan en QSS y widgets para mantener
coherencia.

| Token | Valor | Uso |
|-------|-------|-----|
| `PRIMARY` | `#005A9C` | Acciones principales, navegación |
| `SUCCESS` | `#22A63A` | Confirmaciones, estados positivos |
| `INFO` | `#2F80ED` | Mensajes informativos |
| `WARNING` | `#F2A900` | Advertencias |
| `DANGER` | `#D92D20` | Errores y urgencia alta |
| `SURFACE` | `#F4F8FB` | Fondo general |
| `TEXT` | `#102A43` | Texto principal |
| `TEXT_SECONDARY` | `#52616B` | Texto secundario |
| `BORDER` | `#D9E2EC` | Bordes y separadores |

Tipografía recomendada: **Inter**, con respaldo en Segoe UI, Roboto y Arial.

## Estructura del proyecto

```
desktop/
├── requirements.txt
├── README.md
└── src/
    ├── main/
    │   └── main.py                       # Punto de entrada · contenedor DI
    ├── assets/
    │   └── logo.svg                      # Identidad gráfica
    ├── styles/
    │   └── main.qss                      # Hoja de estilos global
    ├── widgets/
    │   ├── buttons.py                    # Botones primario, success, secondary, outline
    │   └── badges.py                     # Etiquetas de estado y urgencia
    ├── config/
    │   └── settings.py                   # Variables de entorno
    ├── core/
    │   ├── constants.py
    │   ├── colors.py                     # Tokens de color (guía UI)
    │   ├── rut_validator.py              # Algoritmo módulo 11
    │   └── password_service.py           # Hash + criterios de seguridad
    ├── models/
    │   └── entities.py                   # Usuario, Emergencia, enums
    ├── repositories/
    │   ├── user_repository.py            # Mock en memoria
    │   └── emergency_repository.py       # Mock en memoria con datos seed
    ├── services/
    │   └── api_client.py                 # Cliente HTTP para FastAPI
    ├── controllers/
    │   ├── auth_controller.py            # Coordina login y sesión
    │   └── emergency_controller.py       # Lógica de negocio de reportes
    └── views/
        ├── login_view.py
        ├── dashboard_view.py
        ├── emergency_form_view.py
        ├── emergency_list_view.py
        └── main_window.py                # Shell con sidebar y stack
```

## Aplicación de principios SOLID

| Principio | Aplicación en el proyecto |
|-----------|---------------------------|
| **S** Single Responsibility | `RutValidator` solo valida RUT. `PasswordService` solo gestiona contraseñas. Cada widget cumple una sola tarea visual. |
| **O** Open/Closed | Nuevos `TipoEmergencia` o `EstadoEmergencia` se agregan extendiendo enums sin modificar código existente. |
| **L** Liskov Substitution | Cualquier implementación que cumpla la interfaz de `EmergencyRepository` puede sustituirla (memoria, MySQL, mock para tests). |
| **I** Interface Segregation | Las vistas reciben solo el controlador que necesitan. |
| **D** Dependency Inversion | `main.py` instancia los repositorios y los inyecta en los controladores; los controladores se inyectan en las vistas. |

## Próximos pasos

- Conectar `AuthController` y `EmergencyController` con el backend FastAPI a través de `ApiClient`.
- Agregar tabla de historial de cambios de estado (`emergency_status_history`).
- Refinar componentes según feedback del equipo y la presentación del 19 de mayo.
