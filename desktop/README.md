# Aplicación desktop VecinoSeguro

Aplicación de escritorio de **VecinoSeguro**, desarrollada con
**Python + PySide6** e integrada con el backend FastAPI para autenticación
y gestión de emergencias.

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
python -m src.main.main
```

La app lee `API_BASE_URL` desde variables de entorno. Si no se define,
usa `http://localhost:8000`.

Para iniciar sesión y operar con datos reales, levanta primero el backend
FastAPI:

```powershell
cd D:\Trabajos2026\vecino-seguro\backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main.main:app --reload
```

Luego inicia el desktop desde la raíz del proyecto:

```powershell
cd D:\Trabajos2026\vecino-seguro
.\desktop\.venv\Scripts\Activate.ps1
cd desktop
python -m src.main.main
```

Para iniciar sesión en desktop, el backend FastAPI debe estar levantado y la
base de datos debe contener usuarios con contraseñas válidas. En desarrollo,
usa credenciales existentes en la base cargada con `database/seed.sql` o en los
datos reales del entorno local.

## Pantallas implementadas

- **Login** conectado al backend real, con validación de RUT (módulo 11) y
  mensajes de error claros.
- **Dashboard** con KPIs por estado, accesos rápidos y reportes recientes.
- **Formulario de registro de emergencia** con validaciones de negocio.
- **Listado de emergencias** con filtro por estado y panel de detalle.
- **Detalle del reporte** con cambio de estado disponible solo para administradores.
- **Registro básico de usuarios** visible solo para administradores.

## Integración con backend

El login usa el flujo `Vista → AuthController → ApiClient → FastAPI` y consume:

- `POST /api/v1/auth/login` para autenticar usuarios reales por RUT y
  contraseña.

El formulario de emergencias usa el flujo `Vista → EmergencyController →
ApiClient → FastAPI` y consume:

- `GET /api/v1/emergencies/catalogs` para cargar tipos y niveles válidos.
- `POST /api/v1/emergencies/` para registrar emergencias reales.
- `GET /api/v1/emergencies/` para refrescar dashboard y listado.
- `PATCH /api/v1/emergencies/{emergency_id}/status` para cambiar estados reales
  desde el panel administrador.

El formulario de usuarios usa el flujo `Vista → UserController → ApiClient →
FastAPI` y consume:

- `POST /api/v1/users/` para registrar usuarios reales con RUT, nombre, email,
  contraseña inicial y rol.

El desktop no envía `status`; el backend asigna el estado inicial
`pendiente`.

En el listado de emergencias, los administradores pueden actualizar una
emergencia real a `Pendiente`, `En revisión` o `Resuelto`. El estado `Atendido`
permanece solo en el mock local y no se envía al backend hasta que exista en la
API. La observación opcional viaja como `comment`, pero el backend actual no la
persiste; queda reservada para una futura issue de historial.

Después de un login exitoso, el desktop construye un `Usuario` local con el
`id`, `rut`, `full_name`, `email` y `role_id` retornados por el backend. El
rol `role_id=1` se interpreta como administrador y `role_id=2` como vecino.

Los administradores ven el acceso lateral **Usuarios** y pueden crear cuentas
con rol **Vecino** (`role_id=2`) o **Administrador** (`role_id=1`). Los vecinos
no ven ese acceso en la navegación normal. La contraseña inicial no se muestra
ni se guarda en desktop; el backend la persiste como hash bcrypt.

Respuesta segura esperada desde `POST /api/v1/users/`:

```json
{
  "id": 4,
  "rut": "12345678-5",
  "full_name": "Nuevo Vecino",
  "email": "nuevo.vecino@vecinoseguro.cl",
  "role_id": 2
}
```

Códigos esperados: `201`, `400`, `409` y `500`.

Limitación temporal: el backend aún no implementa autorización con token para
este endpoint. En esta etapa el control de acceso se aplica desde desktop,
mostrando el formulario solo a administradores.

Credenciales de administrador para prueba local:

```text
RUT: 11.111.111-1
Contraseña: admin1234
```

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
    │   ├── emergency_controller.py       # Lógica de negocio de reportes
    │   └── user_controller.py            # Lógica de alta básica de usuarios
    └── views/
        ├── login_view.py
        ├── dashboard_view.py
        ├── emergency_form_view.py
        ├── emergency_list_view.py
        ├── user_form_view.py
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

- Agregar tabla de historial de cambios de estado (`emergency_status_history`).
- Refinar componentes según feedback del equipo y la presentación del 19 de mayo.
