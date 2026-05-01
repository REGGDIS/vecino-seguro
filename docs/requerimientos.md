# Requerimientos del prototipo

## Requerimientos funcionales

- Permitir inicio de sesión con RUT y contraseña.
- Permitir registrar emergencias con tipo, descripción, ubicación y nivel de urgencia.
- Permitir visualizar emergencias reportadas.
- Permitir revisar el estado de una emergencia.
- Permitir generar resúmenes o reportes básicos para administración.

## Requerimientos no funcionales

- Mantener una arquitectura modular y mantenible.
- Separar responsabilidades entre rutas, servicios, repositorios y vistas.
- Evitar credenciales reales en el repositorio.
- Usar MySQL como base de datos central.
- Preparar pruebas automatizadas desde etapas tempranas.

## Roles de usuario

- Vecino: reporta emergencias y revisa estados.
- Administrador: gestiona reportes, revisa estados y consulta resúmenes.

## Alcance del prototipo

El prototipo inicial busca demostrar la estructura profesional del sistema y preparar los puntos principales de integración. No incluye todavía autenticación real, persistencia completa ni flujos avanzados.

