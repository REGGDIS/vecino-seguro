# Aplicacion movil VecinoSeguro

Avance inicial de la app movil de VecinoSeguro, preparada con Expo SDK 54, React Native y TypeScript para uso con la version actual de Expo Go.

VecinoSeguro permite reportar, visualizar y organizar emergencias locales de forma rapida, clara y colaborativa. Esta version conecta el login movil y el listado de emergencias con el backend FastAPI real, manteniendo la creacion movil de emergencias como flujo simulado.

## Requisitos

- Node.js compatible con Expo SDK 54.
- npm.
- Expo Go actualizado.

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

La app lee la URL base del backend desde variables publicas de Expo. No se debe versionar un `.env` real.

```text
EXPO_PUBLIC_API_URL=http://localhost:8000
```

El login movil consume `POST /api/v1/auth/login` y el Home/listado de emergencias consumen `GET /api/v1/emergencies/`, por lo que requiere que FastAPI este levantado y accesible desde el dispositivo donde corre Expo.

Para web o ciertos emuladores, `localhost` puede funcionar. En un telefono fisico con Expo Go, `localhost` apunta al telefono y no al PC; usa la IP local del computador conectado a la misma red WiFi:

```text
EXPO_PUBLIC_API_URL=http://192.168.1.11:8000
```

Si pruebas desde un telefono fisico, levanta el backend escuchando en todas las interfaces para que Expo Go pueda alcanzarlo desde la red local:

```bash
uvicorn app.main.main:app --host 0.0.0.0 --port 8000 --reload
```

Credenciales de desarrollo disponibles con la base cargada desde `database/seed.sql`:

```text
Administrador
RUT: 11.111.111-1
Contrasena: admin1234

Vecino
RUT: 22.222.222-2
Contrasena: vecino1234
```

## Alcance actual

- Login movil real con RUT y contrasena contra `POST /api/v1/auth/login`.
- Validacion basica local de formato de RUT antes de autenticar.
- Estado de usuario autenticado en memoria mientras la app esta abierta.
- Home/dashboard con resumen de emergencias reales desde `GET /api/v1/emergencies/`.
- Listado de emergencias reales desde `GET /api/v1/emergencies/`.
- Formulario visual para registrar emergencia, aun simulado en mobile.
- Componentes reutilizables para boton, tarjeta, badge de estado y layout base.
- Paleta visual alineada a la identidad de VecinoSeguro.
- Cliente API preparado para consumir endpoints de FastAPI.

## Funcionalidades simuladas

- El registro de emergencias muestra confirmacion visual, pero no persiste en backend.
- Las emergencias creadas desde el formulario simulado no aparecen todavia en el listado real.
- La creacion real de emergencias desde mobile se implementara en una etapa posterior.

## Fuera de alcance en esta etapa

- Geolocalizacion real.
- Mapas.
- Notificaciones push.
- Persistencia real desde mobile.
- Persistencia de sesion con AsyncStorage.
- Creacion de emergencias reales desde mobile.
- Chat, roles avanzados o integraciones institucionales.

## Estructura relevante

- `app/`: punto de entrada para Expo Router.
- `src/components/`: componentes reutilizables.
- `src/data/`: datos simulados usados por flujos aun no conectados al backend.
- `src/screens/`: pantallas principales.
- `src/services/`: comunicación con FastAPI.
- `src/styles/`: tokens visuales de la app.
- `src/types/`: tipos compartidos de TypeScript.
- `src/config/`: configuración de entorno.
