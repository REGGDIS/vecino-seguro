# Backend VecinoSeguro

Backend desarrollado con Python y FastAPI para la plataforma VecinoSeguro.

Este proyecto incluye autenticación real con RUT y contraseña, gestión de emergencias, reportes agregados para dashboard y documentación automática mediante Swagger.

---

# Requisitos previos

Antes de ejecutar el backend, asegúrate de contar con:

* Python instalado.
* PowerShell o terminal disponible.
* MySQL/MariaDB funcionando localmente.
* Base de datos creada e inicializada con los scripts del proyecto.
* Entorno virtual de Python dentro de `backend/.venv`.
* Dependencias instaladas desde `requirements.txt`.

---

# Instalación y entorno virtual

Desde la raíz del proyecto:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

# Variables de entorno

El backend utiliza variables de entorno para configurar la aplicación y la conexión a MySQL/MariaDB.

Crea un archivo `.env` dentro de `backend/` usando `.env.example` como referencia.

Variables principales:

* `APP_NAME`: nombre de la aplicación.
* `APP_ENV`: ambiente de ejecución.
* `DEBUG`: activa o desactiva modo debug.
* `DATABASE_HOST`: host de la base de datos.
* `DATABASE_PORT`: puerto de MySQL/MariaDB.
* `DATABASE_NAME`: nombre de la base de datos local.
* `DATABASE_USER`: usuario de MySQL/MariaDB.
* `DATABASE_PASSWORD`: contraseña del usuario configurado.

Ejemplo:

```env
APP_NAME=VecinoSeguro
APP_ENV=development
DEBUG=true
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_NAME=vecino_seguro
DATABASE_USER=root
DATABASE_PASSWORD=
```

Importante:

* El archivo `.env` no debe subirse al repositorio.
* No compartir credenciales privadas ni de producción.

---

# Base de datos local

Antes de probar endpoints que consultan MySQL/MariaDB, se debe crear la base de datos local e importar los scripts del proyecto.

Pasos:

1. Crear la base de datos indicada en `.env`.
2. Ejecutar `database/schema.sql`.
3. Ejecutar `database/seed.sql`.

Los datos cargados desde `seed.sql` permiten probar login, emergencias y reportes locales.

No modificar `database/schema.sql` ni `database/seed.sql` desde tareas de documentación.

---

# Ejecución del backend

Con el entorno virtual activado, ejecutar:

```powershell
uvicorn app.main.main:app --reload
```

Por defecto, el backend queda disponible en:

```text
http://127.0.0.1:8000
```

---

# Swagger

FastAPI genera documentación automática en:

```text
http://127.0.0.1:8000/docs
```

Desde Swagger se pueden revisar y probar los endpoints disponibles del backend.

---

# Credenciales reales de desarrollo

Las siguientes credenciales están definidas para pruebas locales en `database/seed.sql`.

## Administrador

```text
RUT: 11.111.111-1
Contraseña: admin1234
```

## Vecino

```text
RUT: 22.222.222-2
Contraseña: vecino1234
```

Estas credenciales son solo para desarrollo local y no deben usarse en producción.

Las credenciales mock antiguas del desktop ya no aplican:

```text
Admin123
Vecino123
```

---

# Endpoints principales actuales

```http
GET /health
GET /api/v1/system/info
POST /api/v1/auth/login
GET /api/v1/users/
POST /api/v1/users/
PATCH /api/v1/users/{user_id}
GET /api/v1/emergencies/
GET /api/v1/emergencies/summary
GET /api/v1/emergencies/recent?limit=4
GET /api/v1/emergencies/catalogs
GET /api/v1/emergencies/{emergency_id}
POST /api/v1/emergencies/
PATCH /api/v1/emergencies/{emergency_id}/status
DELETE /api/v1/emergencies/{emergency_id}
GET /api/v1/reports/summary
GET /api/v1/reports/dashboard-cards
```

Todos estos endpoints pueden revisarse desde Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# Endpoint inicial

```text
GET /health
```

Este endpoint permite verificar que la API está levantada correctamente.

---

# Endpoint de información del sistema

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

---

# Login real con RUT y contraseña

El backend autentica usuarios contra MySQL/MariaDB usando RUT chileno y contraseña bcrypt.

Endpoint:

```text
POST /api/v1/auth/login
```

Body de prueba para administrador:

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

Body de prueba para vecino:

```json
{
  "rut": "22222222-2",
  "password": "vecino1234"
}
```

---

# Gestión básica de usuarios

El módulo `users` permite listar, crear y editar usuarios reales desde el panel
administrador desktop.

## Listar usuarios

Endpoint:

```text
GET /api/v1/users/
```

Devuelve usuarios reales desde MySQL/MariaDB con una respuesta segura. No
incluye `password` ni `password_hash`.

Ejemplo:

```json
[
  {
    "id": 1,
    "rut": "11111111-1",
    "full_name": "Administradora Vecinal",
    "email": "admin@vecinoseguro.cl",
    "role_id": 1,
    "role": "admin"
  },
  {
    "id": 2,
    "rut": "22222222-2",
    "full_name": "Carlos Pérez Soto",
    "email": "carlos.perez@vecinoseguro.cl",
    "role_id": 2,
    "role": "vecino"
  }
]
```

Respuestas esperadas:

* `200 OK`: listado obtenido correctamente.
* `500 Internal Server Error`: error no controlado al consultar usuarios.

Limitación temporal: este endpoint aún no exige token ni permisos backend. Por
ahora el acceso se restringe desde la app desktop mostrando la vista solo a
usuarios con rol administrador. La autorización backend avanzada queda para una
etapa posterior.

## Crear usuarios

Endpoint:

```text
POST /api/v1/users/
```

Body de ejemplo:

```json
{
  "rut": "12.345.678-5",
  "full_name": "Nuevo Vecino",
  "email": "nuevo.vecino@vecinoseguro.cl",
  "password": "Vecino1234",
  "role_id": 2
}
```

Roles válidos en esta etapa:

* `1`: administrador.
* `2`: vecino.

Respuesta segura:

```json
{
  "id": 4,
  "rut": "12345678-5",
  "full_name": "Nuevo Vecino",
  "email": "nuevo.vecino@vecinoseguro.cl",
  "role_id": 2
}
```

La respuesta nunca incluye `password` ni `password_hash`. La contraseña se
guarda en MySQL/MariaDB como hash bcrypt.

Respuestas esperadas:

* `201 Created`: usuario creado.
* `400 Bad Request`: RUT, email, contraseña, nombre o rol inválido.
* `409 Conflict`: RUT o email duplicado.
* `500 Internal Server Error`: error no controlado.

Limitación temporal: este endpoint aún no exige token ni permisos backend. Por
ahora el acceso se restringe desde la app desktop mostrando el formulario solo a
usuarios con rol administrador. La autorización backend avanzada queda para una
etapa posterior.

## Editar usuarios

Endpoint:

```text
PATCH /api/v1/users/{user_id}
```

Permite actualizar solo datos básicos del usuario:

* nombre completo;
* email;
* rol.

No permite editar RUT ni contraseña, y la respuesta nunca incluye `password` ni
`password_hash`.

Body de ejemplo:

```json
{
  "full_name": "Nombre Actualizado",
  "email": "correo.actualizado@vecinoseguro.cl",
  "role_id": 2
}
```

Respuesta segura:

```json
{
  "id": 5,
  "rut": "12345678-5",
  "full_name": "Nombre Actualizado",
  "email": "correo.actualizado@vecinoseguro.cl",
  "role_id": 2,
  "role": "vecino"
}
```

Respuestas esperadas:

* `200 OK`: usuario actualizado.
* `400 Bad Request`: nombre, email o rol inválido.
* `404 Not Found`: usuario inexistente.
* `409 Conflict`: email perteneciente a otro usuario.
* `500 Internal Server Error`: error no controlado.

Limitación temporal: este endpoint aún no exige token ni permisos backend. Por
ahora el acceso se restringe desde la app desktop mostrando la vista solo a
usuarios con rol administrador. La autorización backend avanzada queda para una
etapa posterior.

---

# Endpoints de emergencias

## Listar emergencias

```text
GET /api/v1/emergencies/
```

Devuelve el listado de emergencias almacenadas en MySQL/MariaDB, ordenadas por fecha de creación descendente.

Ejemplo:

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

---

## Resumen optimizado para dashboard

```text
GET /api/v1/emergencies/summary
```

Devuelve contadores por estado sin transferir todo el listado de emergencias.
Este endpoint optimiza la carga de KPIs del dashboard desktop.

Ejemplo:

```json
{
  "pendiente": 2,
  "en_revision": 1,
  "atendido": 0,
  "resuelto": 3
}
```

Nota: `atendido` se devuelve en `0` por compatibilidad con el dashboard
desktop; el backend actual no lo maneja como estado válido.

---

## Emergencias recientes para dashboard

```text
GET /api/v1/emergencies/recent?limit=4
```

Devuelve las emergencias más recientes, ordenadas por fecha de creación
descendente, sin consultar todo el historial. Este endpoint optimiza la sección
de reportes recientes del dashboard desktop. El parámetro `limit` se acota entre
`1` y `20`.

Ejemplo:

```json
[
  {
    "id": 4,
    "user_id": 2,
    "type": "incendio",
    "description": "Humo visible en una vivienda cercana",
    "location": "Pasaje Los Aromos 123",
    "urgency_level": "alta",
    "status": "pendiente",
    "created_at": "2026-05-04T14:00:00",
    "updated_at": null
  }
]
```

---

## Catálogos de emergencias

```text
GET /api/v1/emergencies/catalogs
```

Devuelve catálogos fijos para formularios y filtros de emergencias.

Ejemplo:

```json
{
  "emergency_types": [
    { "value": "robo", "label": "Robo" },
    { "value": "incendio", "label": "Incendio" }
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

---

## Crear emergencia

```text
POST /api/v1/emergencies/
```

Crea una emergencia real en MySQL/MariaDB.

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

---

## Actualizar estado de emergencia

```text
PATCH /api/v1/emergencies/{emergency_id}/status
```

Estados válidos:

* `pendiente`
* `en_revision`
* `resuelto`

Body de ejemplo:

```json
{
  "status": "en_revision",
  "comment": "Reporte revisado desde panel administrador."
}
```

Respuestas esperadas:

* `200 OK`
* `400 Bad Request`
* `404 Not Found`
* `500 Internal Server Error`

---

## Eliminar emergencia

```text
DELETE /api/v1/emergencies/{emergency_id}
```

Elimina una emergencia real por ID desde la tabla `emergencies`. Su uso
previsto es el panel administrador de la aplicación desktop.

Respuestas esperadas:

* `204 No Content`: emergencia eliminada correctamente, sin body de respuesta.
* `404 Not Found`: la emergencia no existe.
* `500 Internal Server Error`: error no controlado.

No requiere cambios en `database/schema.sql`. Si existen registros asociados en
`emergency_status_history`, la relación con `ON DELETE CASCADE` se encarga de
eliminarlos junto con la emergencia.

Limitación temporal: igual que otras acciones administrativas actuales, este
endpoint aún no exige token ni permisos backend. En esta etapa el acceso se
restringe desde la app desktop mostrando la acción solo a administradores.

---

## Detalle de emergencia

```text
GET /api/v1/emergencies/{emergency_id}
```

Ejemplo:

```text
http://127.0.0.1:8000/api/v1/emergencies/1
```

Respuesta exitosa:

```json
{
  "id": 1,
  "user_id": 2,
  "type": "Incendio",
  "description": "Humo visible cerca de una vivienda. Vecinos reportan llamas en el techo.",
  "location": "Pasaje Los Alerces 123, Villa El Bosque",
  "urgency_level": "alta",
  "status": "pendiente",
  "created_at": "2026-05-04T14:00:00",
  "updated_at": "2026-05-04T14:00:00"
}
```

Respuesta de error:

```json
{
  "detail": "Emergencia no encontrada"
}
```

---

# Endpoints de reportes

## Resumen para dashboard

```text
GET /api/v1/reports/summary
```

Entrega un resumen general de emergencias registradas en MySQL/MariaDB.

La respuesta incluye:

* Total de emergencias.
* Conteo por estado.
* Conteo por nivel de urgencia.

---

## Tarjetas de dashboard

```text
GET /api/v1/reports/dashboard-cards
```

Entrega tarjetas simplificadas para dashboard desktop o móvil.

Ejemplo de respuesta:

```json
{
  "cards": [
    {
      "key": "total",
      "label": "Emergencias totales",
      "value": 4
    },
    {
      "key": "pendiente",
      "label": "Pendientes",
      "value": 2
    }
  ]
}
```

---

# Pruebas manuales sugeridas

1. Levantar el backend con Uvicorn.
2. Abrir `http://127.0.0.1:8000/health`.
3. Abrir `http://127.0.0.1:8000/docs`.
4. Probar login real con las credenciales de desarrollo.
5. Probar `GET /api/v1/users/` y confirmar que lista usuarios reales sin
   `password_hash`.
6. Probar `POST /api/v1/users/` con usuario vecino y administrador.
7. Probar errores de RUT inválido, RUT duplicado, email duplicado y contraseña corta.
8. Confirmar que la respuesta de creación no incluya `password_hash`.
9. Probar `PATCH /api/v1/users/{user_id}` con nombre, email y rol válidos.
10. Probar errores de usuario inexistente, email duplicado y rol inválido.
11. Confirmar que la respuesta de edición no incluya `password_hash`.
12. Probar `GET /api/v1/emergencies/`.
13. Probar `GET /api/v1/emergencies/summary`.
14. Probar `GET /api/v1/emergencies/recent?limit=4`.
15. Probar `GET /api/v1/emergencies/catalogs`.
16. Probar `GET /api/v1/reports/summary`.
17. Probar `GET /api/v1/reports/dashboard-cards`.
18. Verificar que las respuestas sean coherentes con los datos cargados desde `database/seed.sql`.

---

# Módulos preparados

* `auth`: autenticación con RUT y contraseña.
* `users`: gestión de usuarios.
* `emergencies`: registro y seguimiento de emergencias.
* `reports`: reportes, estadísticas y resúmenes.

---

# Notas importantes

* No subir `.env` al repositorio.
* No compartir credenciales privadas.
* Las credenciales documentadas son solo para desarrollo.
* Swagger es la forma recomendada para probar endpoints.
* Mantener sincronizado el backend con `main` antes de crear nuevas ramas.
