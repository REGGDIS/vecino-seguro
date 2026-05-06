# Base de datos VecinoSeguro

Esta carpeta contiene los scripts iniciales de la base de datos MySQL del prototipo VecinoSeguro. La base se llama `vecino_seguro` y agrupa la información sobre roles, usuarios, emergencias e historial de cambios de estado.

## Contenido

| Archivo | Propósito |
|---------|-----------|
| `schema.sql` | Crea la base de datos y las tablas principales con sus claves primarias, foráneas, índices y restricciones. |
| `seed.sql` | Inserta datos de prueba para desarrollo y demostración (roles, usuarios, emergencias y un historial de ejemplo). |
| `README.md` | Este archivo: explica el contenido y cómo ejecutar los scripts. |

## Modelo de datos

El esquema define cuatro tablas relacionadas:

### `roles`
Catálogo de roles del sistema. Por ahora se usan dos: `admin` y `vecino`.

### `users`
Usuarios del sistema. Cada usuario tiene un RUT único, correo, nombre completo, contraseña almacenada como hash y un rol asignado mediante `role_id`.

### `emergencies`
Emergencias reportadas por los vecinos. Cada emergencia tiene un tipo, descripción, ubicación, nivel de urgencia (`baja`, `media`, `alta`, `critica`) y estado del ciclo de vida (`pendiente`, `en_revision`, `resuelto`).

### `emergency_status_history`
Auditoría de los cambios de estado de cada emergencia. Permite saber quién cambió un estado, cuándo y opcionalmente con qué comentario.

### Relaciones principales

```
roles (1) ──── (N) users
users (1) ──── (N) emergencies
emergencies (1) ──── (N) emergency_status_history
users (1) ──── (N) emergency_status_history (changed_by)
```

## Cómo ejecutar los scripts

Los scripts se ejecutan en orden: primero `schema.sql` (estructura), luego `seed.sql` (datos). Existen tres alternativas equivalentes según la herramienta que tengas instalada.

### Opción A — Consola MySQL

Desde la terminal, ubicado en la carpeta `database/`:

```bash
mysql -u root -p < schema.sql
mysql -u root -p vecino_seguro < seed.sql
```

Reemplaza `root` por tu usuario si corresponde.

### Opción B — MySQL Workbench

1. Abre MySQL Workbench y conéctate a tu servidor local.
2. Menú `File → Open SQL Script`, selecciona `schema.sql` y ejecútalo con el botón del rayo (`Ctrl + Shift + Enter`).
3. Repite el proceso con `seed.sql`.

### Opción C — phpMyAdmin (XAMPP, WAMP o Laragon)

1. Inicia el servicio MySQL/MariaDB desde el panel de control.
2. Abre `http://localhost/phpmyadmin` en el navegador.
3. Pestaña `Importar`, selecciona `schema.sql` y ejecuta.
4. Selecciona la base `vecino_seguro` desde el menú lateral.
5. Pestaña `Importar` nuevamente, selecciona `seed.sql` y ejecuta.

## Notas de arquitectura

De acuerdo con `docs/arquitectura.md`, **únicamente el backend FastAPI se conecta directamente a MySQL**. La aplicación desktop (PySide6) y la aplicación móvil (Expo + React Native) consumen los datos a través de la API HTTP del backend, no acceden directamente a la base de datos.

Este principio mantiene la lógica de negocio centralizada y evita que cada cliente tenga que conocer el esquema de datos.

## Notas de seguridad

- **Todos los datos del seed son ficticios.** RUTs, nombres, correos y direcciones son inventados solo para demostración.
- **Las contraseñas se almacenan como hash**, nunca en texto plano. Los hashes incluidos en `seed.sql` son valores de ejemplo identificables y **no representan contraseñas reales**.
- En producción, las contraseñas deben generarse con un algoritmo de hash seguro como **bcrypt** o **argon2**, incluyendo un `salt` único por contraseña.
- **Nunca incluir credenciales reales en el repositorio**: ni en `seed.sql`, ni en archivos `.env` versionados.

## Compatibilidad

| Aspecto | Valor |
|---------|-------|
| Motor de base de datos | MySQL 8.0+ (recomendado) |
| Compatible con | MariaDB 10.4+ (probado en XAMPP) |
| Charset | `utf8mb4` |
| Cotejamiento | `utf8mb4_unicode_ci` |
| Motor de almacenamiento | `InnoDB` (requerido para soportar claves foráneas) |

## Estructura para iteraciones futuras

Si en iteraciones posteriores se requieren consultas de ejemplo, vistas o procedimientos almacenados, conviene agregar archivos complementarios manteniendo la convención de nombres en inglés:

- `queries_examples.sql` — consultas frecuentes documentadas
- `views.sql` — vistas para reportes
- `procedures.sql` — procedimientos almacenados