# Aplicacion movil VecinoSeguro

Avance inicial de la app movil de VecinoSeguro, preparada con Expo SDK 54, React Native y TypeScript para uso con la version actual de Expo Go.

VecinoSeguro permite reportar, visualizar y organizar emergencias locales de forma rapida, clara y colaborativa. Esta version no conecta todavia con el backend real; deja armado el flujo visual y la base tecnica para integracion futura con FastAPI.

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

## Alcance actual

- Login movil visual con RUT y contrasena.
- Validacion basica de formato de RUT para el flujo simulado.
- Home/dashboard con resumen de emergencias.
- Formulario visual para registrar emergencia.
- Listado inicial de emergencias con datos mock.
- Componentes reutilizables para boton, tarjeta, badge de estado y layout base.
- Paleta visual alineada a la identidad de VecinoSeguro.
- Cliente API inicial preparado para futura integracion con FastAPI.

## Funcionalidades simuladas

- El inicio de sesion no consulta credenciales reales.
- El registro de emergencias muestra confirmacion visual, pero no persiste en backend.
- Los reportes se cargan desde `src/data/mockEmergencies.ts`.

## Fuera de alcance en esta etapa

- Geolocalizacion real.
- Mapas.
- Notificaciones push.
- Login real contra backend.
- Persistencia real desde mobile.
- Chat, roles avanzados o integraciones institucionales.

## Estructura relevante

- `app/`: punto de entrada para Expo Router.
- `src/components/`: componentes reutilizables.
- `src/data/`: datos simulados para el avance inicial.
- `src/screens/`: pantallas principales.
- `src/services/`: comunicación con FastAPI.
- `src/styles/`: tokens visuales de la app.
- `src/types/`: tipos compartidos de TypeScript.
- `src/config/`: configuración de entorno.
