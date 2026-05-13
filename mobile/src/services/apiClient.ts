import { environment } from "../config/environment";
import type { AuthenticatedUser, LoginResponse } from "../types/auth";

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

interface BackendAuthenticatedUser {
  id: number;
  rut: string;
  full_name: string;
  email: string;
  role_id: number;
}

interface BackendLoginResponse {
  success: boolean;
  message: string;
  user: BackendAuthenticatedUser;
}

const loginNetworkErrorMessage =
  "No fue posible conectar con el backend. Verifica que FastAPI esté en ejecución y que la URL de API sea correcta.";

function normalizeRutForLogin(rut: string) {
  return rut.trim().replace(/\./g, "").toUpperCase();
}

function getLoginErrorMessage(status: number) {
  if (status === 400 || status === 422) {
    return "Revisa el formato del RUT y la contraseña.";
  }

  if (status === 401) {
    return "RUT o contraseña incorrectos.";
  }

  if (status >= 500) {
    return "El backend no pudo procesar el inicio de sesión. Inténtalo nuevamente.";
  }

  return "No fue posible iniciar sesión. Inténtalo nuevamente.";
}

function mapAuthenticatedUser(user: BackendAuthenticatedUser): AuthenticatedUser {
  return {
    email: user.email,
    fullName: user.full_name,
    id: user.id,
    roleId: user.role_id,
    rut: user.rut,
  };
}

function isBackendLoginResponse(data: unknown): data is BackendLoginResponse {
  if (!data || typeof data !== "object") {
    return false;
  }

  const response = data as Partial<BackendLoginResponse>;
  const user = response.user as Partial<BackendAuthenticatedUser> | undefined;

  return (
    typeof response.success === "boolean" &&
    typeof response.message === "string" &&
    !!user &&
    typeof user.id === "number" &&
    typeof user.rut === "string" &&
    typeof user.full_name === "string" &&
    typeof user.email === "string" &&
    typeof user.role_id === "number"
  );
}

export async function login(rut: string, password: string): Promise<LoginResponse> {
  let response: Response;

  try {
    response = await fetch(buildApiUrl("/api/v1/auth/login"), {
      body: JSON.stringify({
        password,
        rut: normalizeRutForLogin(rut),
      }),
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
    });
  } catch {
    throw new Error(loginNetworkErrorMessage);
  }

  if (!response.ok) {
    throw new Error(getLoginErrorMessage(response.status));
  }

  let data: unknown;

  try {
    data = await response.json();
  } catch {
    throw new Error("No fue posible iniciar sesión. Inténtalo nuevamente.");
  }

  if (!isBackendLoginResponse(data) || !data.success) {
    throw new Error("No fue posible iniciar sesión. Inténtalo nuevamente.");
  }

  return {
    message: data.message,
    success: data.success,
    user: mapAuthenticatedUser(data.user),
  };
}
