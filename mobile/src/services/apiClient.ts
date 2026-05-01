import { environment } from "../config/environment";

// Cliente base para consumir la API FastAPI desde React Native.
export async function getHealthStatus() {
  const response = await fetch(`${environment.apiUrl}/health`);

  if (!response.ok) {
    throw new Error("No fue posible consultar el estado del backend.");
  }

  return response.json();
}

