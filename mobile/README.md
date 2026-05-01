# Aplicación móvil VecinoSeguro

Este directorio contiene la estructura inicial de la aplicación móvil, preparada para Expo, React Native y TypeScript.

## Instalación

```bash
cd mobile
npm install
```

## Ejecución

```bash
npm run start
```

También puedes usar:

```bash
npm run android
npm run ios
npm run web
```

## Configuración del backend

Copia `.env.example` a `.env` y ajusta:

```text
EXPO_PUBLIC_API_URL=http://localhost:8000
```

## Estructura preparada

- `app/`: punto de entrada para Expo Router.
- `src/components/`: componentes reutilizables.
- `src/screens/`: pantallas principales.
- `src/services/`: comunicación con FastAPI.
- `src/types/`: tipos compartidos de TypeScript.
- `src/config/`: configuración de entorno.

