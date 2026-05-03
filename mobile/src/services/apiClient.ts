import { environment } from "../config/environment";

const trimTrailingSlash = (value: string) => value.replace(/\/+$/, "");

export const apiBaseUrl = trimTrailingSlash(environment.apiUrl);

export function buildApiUrl(endpoint: string) {
  const normalizedEndpoint = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;

  return `${apiBaseUrl}${normalizedEndpoint}`;
}

// Cliente base preparado para consumir endpoints reales de FastAPI en futuras iteraciones.
export async function getHealthStatus() {
  const response = await fetch(buildApiUrl("/health"));

  if (!response.ok) {
    throw new Error("No fue posible consultar el estado del backend.");
  }

  return response.json();
}
