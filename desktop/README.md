# Aplicación desktop VecinoSeguro

Este directorio contiene la estructura inicial de la aplicación de escritorio en Python. La opción recomendada para el prototipo es PySide6, porque permite construir interfaces profesionales y mantenibles; alternativamente, el equipo puede migrar a Tkinter manteniendo la misma separación entre vistas, controladores, servicios y repositorios.

## Instalación

```bash
cd desktop
python -m venv .venv
pip install -r requirements.txt
```

## Ejecución

```bash
python src/main/main.py
```

## Vistas iniciales preparadas

- `LoginView`: ingreso con RUT y contraseña.
- `DashboardView`: resumen general de emergencias.
- `EmergencyFormView`: formulario para registrar emergencias.

## Organización

La aplicación separa vistas, controladores, servicios, repositorios, configuración y constantes para favorecer mantenibilidad y principios SOLID. Las vistas actuales usan PySide6 como base recomendada, pero están aisladas del resto de capas para que puedan reemplazarse por Tkinter sin rehacer la lógica de controladores o comunicación con el backend.
