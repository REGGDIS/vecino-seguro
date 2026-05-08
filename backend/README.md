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

## Endpoint de emergencias

```text
GET /api/v1/emergencies
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

## Módulos preparados

- `auth`: autenticación con RUT y contraseña.
- `users`: gestión de usuarios.
- `emergencies`: registro y seguimiento de emergencias.
- `reports`: reportes, estadísticas y resúmenes.

## Configuración

Usa `.env.example` como referencia para crear un archivo `.env` local. No se deben versionar credenciales reales.

