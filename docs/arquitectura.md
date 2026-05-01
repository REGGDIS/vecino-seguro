# Arquitectura general

VecinoSeguro se organiza como una solución modular con un backend centralizado y dos clientes principales: aplicación desktop y aplicación móvil.

## Componentes

- Backend FastAPI: expone la API central, valida datos, coordina reglas de negocio y se comunica con MySQL.
- App desktop PySide6: consume la API para permitir gestión y revisión de emergencias desde computadores.
- App móvil Expo + React Native: consume la API para reportar y visualizar emergencias desde dispositivos móviles.
- MySQL: almacena usuarios, roles, emergencias e historial de estados.

## Separación por módulos

El backend se divide en módulos como `auth`, `users`, `emergencies` y `reports`. Cada módulo separa rutas, servicios, repositorios y esquemas para mantener responsabilidades claras.

## Flujo general

1. Un usuario reporta una emergencia desde móvil o desktop.
2. El cliente envía la solicitud al backend FastAPI.
3. El backend valida, aplica reglas de negocio y persiste datos en MySQL.
4. Los clientes consultan reportes, estados y resúmenes desde la API.

