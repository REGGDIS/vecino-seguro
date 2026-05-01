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

## Módulos preparados

- `auth`: autenticación con RUT y contraseña.
- `users`: gestión de usuarios.
- `emergencies`: registro y seguimiento de emergencias.
- `reports`: reportes, estadísticas y resúmenes.

## Configuración

Usa `.env.example` como referencia para crear un archivo `.env` local. No se deben versionar credenciales reales.

