# VecinoSeguro

VecinoSeguro es una plataforma comunitaria que permite reportar, visualizar y gestionar emergencias locales de forma rápida, ordenada y colaborativa, fortaleciendo la seguridad y la respuesta vecinal.

## Descripción

Este repositorio contiene la estructura inicial del proyecto VecinoSeguro, desarrollado para el ramo Taller de Ingeniería de Software. El objetivo del prototipo es integrar un backend centralizado, una aplicación desktop, una aplicación móvil, una base de datos MySQL y documentación técnica para que el equipo pueda comenzar el desarrollo de forma ordenada.

## Integrantes

- Roberto González
- Raymond Civil
- Franco Quezada

## Tecnologías

- MySQL
- Python
- FastAPI
- PySide6
- Expo
- React Native
- TypeScript
- GitHub

## Estructura del repositorio

```text
vecino-seguro/
├── backend/   # API centralizada con Python + FastAPI
├── desktop/   # Aplicación de escritorio con Python + PySide6
├── mobile/    # Aplicación móvil con Expo + React Native + TypeScript
├── database/  # Scripts iniciales para MySQL
├── docs/      # Documentación técnica y de gestión
├── .gitignore
├── LICENSE
└── README.md
```

## Inicio rápido

### Backend

```bash
cd backend
python -m venv .venv
pip install -r requirements.txt
uvicorn app.main.main:app --reload
```

El endpoint inicial disponible es:

```text
GET /health
```

### Desktop

```bash
cd desktop
python -m venv .venv
pip install -r requirements.txt
python src/main/main.py
```

### Mobile

```bash
cd mobile
npm install
npm run start
```

Configura la URL del backend copiando `mobile/.env.example` a un archivo `.env` local y ajustando `EXPO_PUBLIC_API_URL` según corresponda.

## Estado del proyecto

Estructura inicial lista para el primer commit y para comenzar el desarrollo modular del prototipo.

