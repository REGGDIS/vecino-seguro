# Arquitectura general

VecinoSeguro se organiza como una solución modular con un backend centralizado y dos clientes principales: aplicación desktop y aplicación móvil.

## Componentes

- Backend: Python + FastAPI. Expone la API central, valida datos, coordina reglas de negocio y se comunica con MySQL.
- Base de datos: MySQL. Almacena usuarios, roles, emergencias e historial de estados.
- Desktop: Python + PySide6. Consume la API del backend para permitir gestión y revisión de emergencias desde computadores.
- Mobile: Expo + React Native + TypeScript. Consume la API para reportar y visualizar emergencias desde dispositivos móviles.

## Separación por módulos

El backend se divide en módulos como `auth`, `users`, `emergencies` y `reports`. Cada módulo separa rutas, servicios, repositorios y esquemas para mantener responsabilidades claras.

La aplicación desktop se organiza en vistas PySide6, controladores, servicios, recursos visuales y estilos QSS. El cliente desktop no se conecta directamente a MySQL; toda lectura o escritura de datos debe pasar por la API FastAPI del backend.

## Flujo general

1. Un usuario reporta una emergencia desde móvil o desktop.
2. El cliente envía la solicitud al backend FastAPI.
3. El backend valida, aplica reglas de negocio y persiste datos en MySQL.
4. Los clientes consultan reportes, estados y resúmenes desde la API.
