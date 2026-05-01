// Configuración de entorno para centralizar la URL del backend FastAPI.
export const environment = {
  apiUrl: process.env.EXPO_PUBLIC_API_URL ?? "http://localhost:8000",
};

