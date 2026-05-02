# Aplicación desktop VecinoSeguro

Este directorio contiene la estructura inicial de la aplicación de escritorio de VecinoSeguro. La app desktop se desarrollará oficialmente con Python + PySide6, usando una separación clara entre interfaz visual, coordinación de eventos, comunicación con la API y recursos de presentación.

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

La aplicación separa responsabilidades para favorecer mantenibilidad y principios SOLID:

- `views/`: pantallas PySide6 como login, panel principal y formularios.
- `controllers/`: coordinación entre eventos de la interfaz y servicios de aplicación.
- `services/`: comunicación con la API FastAPI y lógica de apoyo externa a las vistas.
- `assets/`: recursos visuales como íconos, imágenes o fuentes.
- `styles/`: estilos QSS para centralizar la identidad visual de la interfaz.
- `repositories/`, `config/` y `core/`: puntos de apoyo para configuración, constantes y adaptadores cuando el prototipo los requiera.

Las vistas PySide6 deben mantenerse enfocadas en construir y actualizar la interfaz. La lógica de negocio y el consumo de API deben residir en controladores y servicios.
