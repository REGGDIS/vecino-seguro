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

Para probar los endpoints desde Swagger:

1. Ejecutar el backend con `uvicorn app.main.main:app --reload`.
2. Abrir `http://127.0.0.1:8000/docs`.
3. Probar `GET /api/v1/emergencies/catalogs`.
4. Probar `POST /api/v1/emergencies/` con el body de ejemplo.
5. Verificar que la nueva emergencia aparezca en `GET /api/v1/emergencies/`.

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


