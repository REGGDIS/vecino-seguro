# Backend VecinoSeguro

Este directorio contiene la estructura inicial del backend de VecinoSeguro, desarrollado con Python y FastAPI. La organización está pensada para separar responsabilidades por configuración, conexión a datos, utilidades compartidas y módulos de negocio.

## Instalación

```bash
cd backend
python -m venv .venv
pip install -r requirements.txt
```

## Ejecución

```bash
uvicorn app.main.main:app --reload
```

## Endpoint inicial

```text
GET /health
```

Este endpoint permite verificar que la API está levantada correctamente.

## Endpoint de información del sistema

```text
GET /api/v1/system/info
```

Entrega información general del backend, incluyendo nombre de la aplicación, versión, ambiente, estado y mensaje operativo.

Ejemplo de respuesta:

```json
{
  "app_name": "VecinoSeguro",
  "version": "0.1.0",
  "environment": "development",
  "status": "running",
  "message": "Backend VecinoSeguro operativo"
}
```

Este endpoint permite verificar que la API está levantada correctamente.

## Endpoints de emergencias

```text
GET /api/v1/emergencies/
```

Devuelve el listado de emergencias almacenadas en MySQL, ordenadas por fecha de creación descendente.

Ejemplo de respuesta:

```json
[
  {
    "id": 1,
    "user_id": 2,
    "type": "Incendio",
    "description": "Humo visible cerca de una vivienda.",
    "location": "Pasaje Los Alerces 123",
    "urgency_level": "alta",
    "status": "pendiente",
    "created_at": "2026-05-04T00:00:00",
    "updated_at": "2026-05-04T00:00:00"
  }
]
```

Antes de probar este endpoint, se debe:

1. Crear la base con `database/schema.sql`.
2. Cargar datos de prueba con `database/seed.sql`.
3. Configurar `backend/.env` usando `backend/.env.example` como referencia.
4. Ejecutar el backend con `uvicorn app.main.main:app --reload`.

Si la base de datos no responde o la consulta falla, el endpoint retorna `500` con un mensaje genérico.

```text
GET /api/v1/emergencies/catalogs
```

Devuelve catálogos fijos para formularios y filtros de emergencias. Este endpoint no consulta MySQL.

Ejemplo de respuesta:

```json
{
  "emergency_types": [
    { "value": "robo", "label": "Robo" },
    { "value": "incendio", "label": "Incendio" },
    { "value": "accidente", "label": "Accidente" },
    { "value": "emergencia_medica", "label": "Emergencia médica" },
    { "value": "corte_luz", "label": "Corte de luz" },
    { "value": "persona_extraviada", "label": "Persona extraviada" },
    { "value": "solicitud_ayuda", "label": "Solicitud de ayuda" },
    { "value": "otro", "label": "Otro" }
  ],
  "urgency_levels": [
    { "value": "baja", "label": "Baja" },
    { "value": "media", "label": "Media" },
    { "value": "alta", "label": "Alta" },
    { "value": "critica", "label": "Crítica" }
  ],
  "statuses": [
    { "value": "pendiente", "label": "Pendiente" },
    { "value": "en_revision", "label": "En revisión" },
    { "value": "resuelto", "label": "Resuelto" }
  ]
}
```

```text
POST /api/v1/emergencies/
```

Crea una emergencia real en MySQL. El backend valida `type` y `urgency_level` contra los catálogos permitidos y asigna automáticamente `status = pendiente`.

Body de ejemplo:

```json
{
  "user_id": 2,
  "type": "incendio",
  "description": "Humo visible en una vivienda cercana",
  "location": "Pasaje Los Aromos 123",
  "urgency_level": "alta"
}
```

Si la creación es correcta, responde `201 Created` con la emergencia creada, incluyendo `id`, `created_at` y `updated_at` generados por la base de datos.

```text
PATCH /api/v1/emergencies/{emergency_id}/status
```

Actualiza el estado real de una emergencia en MySQL/MariaDB y devuelve la
emergencia actualizada con el mismo formato de `EmergencySummary`.

Estados válidos:

- `pendiente`
- `en_revision`
- `resuelto`

Body de ejemplo:

```json
{
  "status": "en_revision",
  "comment": "Reporte revisado desde panel administrador."
}
```

El campo `comment` es opcional. Actualmente viaja en el request pero no se
persiste, porque la tabla `emergencies` no tiene columna de observaciones por
cambio de estado. Queda reservado para una futura issue de historial de
estados.

Respuestas esperadas:

- `200 OK`: estado actualizado.
- `400 Bad Request`: estado inválido.
- `404 Not Found`: emergencia inexistente.
- `500 Internal Server Error`: error inesperado al actualizar.

Para probar los endpoints desde Swagger:

1. Ejecutar el backend con `uvicorn app.main.main:app --reload`.
2. Abrir `http://127.0.0.1:8000/docs`.
3. Probar `GET /api/v1/emergencies/catalogs`.
4. Probar `POST /api/v1/emergencies/` con el body de ejemplo.
5. Probar `PATCH /api/v1/emergencies/{emergency_id}/status` con un id existente.
6. Verificar que la emergencia aparezca actualizada en `GET /api/v1/emergencies/`.

## Login real con RUT y contraseña

El backend autentica usuarios contra MySQL/MariaDB usando RUT chileno y contraseña bcrypt.

Antes de probar el login:

1. Instalar dependencias desde `backend/`.
   ```bash
   pip install -r requirements.txt
   ```
2. Configurar `backend/.env` usando `backend/.env.example` como referencia.
3. Cargar la estructura de base de datos con `database/schema.sql`.
4. Cargar datos ficticios de desarrollo con `database/seed.sql`.
5. Ejecutar el backend desde `backend/`.
   ```bash
   uvicorn app.main.main:app --reload
   ```

Endpoint:

```text
POST /api/v1/auth/login
```

Body de prueba para usuario administrador:

```json
{
  "rut": "11111111-1",
  "password": "admin1234"
}
```

Respuesta esperada:

```json
{
  "success": true,
  "message": "Login exitoso",
  "user": {
    "id": 1,
    "rut": "11111111-1",
    "full_name": "Administradora Vecinal",
    "email": "admin@vecinoseguro.cl",
    "role_id": 1
  }
}
```

También existe un usuario vecino de prueba:

```json
{
  "rut": "22222222-2",
  "password": "vecino1234"
}
```

Estas credenciales son ficticias y solo sirven para desarrollo y demostración.

## Módulos preparados

- `auth`: autenticación con RUT y contraseña.
- `users`: gestión de usuarios.
- `emergencies`: registro y seguimiento de emergencias.
- `reports`: reportes, estadísticas y resúmenes.

## Configuración

Usa `.env.example` como referencia para crear un archivo `.env` local. No se deben versionar credenciales reales.


## Endpoint de resumen para dashboard

```text
GET /api/v1/reports/summary
```

Entrega un resumen general de emergencias registradas en MySQL/MariaDB.

La respuesta incluye:

- Total de emergencias.
- Conteo por estado.
- Conteo por nivel de urgencia.

Este endpoint es de solo lectura y está pensado para ser consumido posteriormente por el dashboard desktop o móvil.


