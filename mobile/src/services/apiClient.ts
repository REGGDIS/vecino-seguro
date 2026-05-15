import { environment } from "../config/environment";
import type { AuthenticatedUser, LoginResponse } from "../types/auth";
import type {
  BackendEmergency,
  BackendEmergencyCatalogs,
  CatalogOption,
  CreateBackendEmergencyInput,
  EmergencyCatalogs,
} from "../types/emergency";

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
const emergenciesNetworkErrorMessage =
  "No fue posible cargar las emergencias. Verifica que el backend esté disponible y que la URL de API sea correcta.";
const emergencyCatalogsNetworkErrorMessage =
  "No fue posible cargar las opciones del formulario. Verifica que el backend esté disponible.";
const createEmergencyNetworkErrorMessage =
  "No fue posible registrar la emergencia. Verifica que el backend esté disponible.";

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

function isBackendEmergency(data: unknown): data is BackendEmergency {
  if (!data || typeof data !== "object") {
    return false;
  }

  const emergency = data as Partial<BackendEmergency>;

  return (
    typeof emergency.id === "number" &&
    typeof emergency.user_id === "number" &&
    typeof emergency.type === "string" &&
    typeof emergency.description === "string" &&
    typeof emergency.location === "string" &&
    typeof emergency.urgency_level === "string" &&
    typeof emergency.status === "string" &&
    typeof emergency.created_at === "string" &&
    (typeof emergency.updated_at === "string" || emergency.updated_at === null)
  );
}

function isCatalogOption(data: unknown): data is CatalogOption {
  if (!data || typeof data !== "object") {
    return false;
  }

  const option = data as Partial<CatalogOption>;

  return typeof option.value === "string" && typeof option.label === "string";
}

function isBackendEmergencyCatalogs(data: unknown): data is BackendEmergencyCatalogs {
  if (!data || typeof data !== "object") {
    return false;
  }

  const catalogs = data as Partial<BackendEmergencyCatalogs>;

  return (
    Array.isArray(catalogs.emergency_types) &&
    catalogs.emergency_types.every(isCatalogOption) &&
    Array.isArray(catalogs.urgency_levels) &&
    catalogs.urgency_levels.every(isCatalogOption) &&
    Array.isArray(catalogs.statuses) &&
    catalogs.statuses.every(isCatalogOption)
  );
}

function mapEmergencyCatalogs(catalogs: BackendEmergencyCatalogs): EmergencyCatalogs {
  return {
    emergencyTypes: catalogs.emergency_types,
    urgencyLevels: catalogs.urgency_levels,
  };
}

async function getBackendErrorMessage(response: Response, fallbackMessage: string) {
  try {
    const data = (await response.json()) as { detail?: unknown };

    if (typeof data.detail === "string" && data.detail.trim()) {
      return data.detail;
    }
  } catch {
    return fallbackMessage;
  }

  return fallbackMessage;
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

export async function getBackendEmergencies(): Promise<BackendEmergency[]> {
  let response: Response;

  try {
    response = await fetch(buildApiUrl("/api/v1/emergencies/"));
  } catch {
    throw new Error(emergenciesNetworkErrorMessage);
  }

  if (!response.ok) {
    throw new Error("No fue posible cargar las emergencias desde el backend.");
  }

  let data: unknown;

  try {
    data = await response.json();
  } catch {
    throw new Error("El backend devolvió una respuesta de emergencias inválida.");
  }

  if (!Array.isArray(data) || !data.every(isBackendEmergency)) {
    throw new Error("El backend devolvió una respuesta de emergencias inválida.");
  }

  return data;
}

export async function getEmergencyCatalogs(): Promise<EmergencyCatalogs> {
  let response: Response;

  try {
    response = await fetch(buildApiUrl("/api/v1/emergencies/catalogs"));
  } catch {
    throw new Error(emergencyCatalogsNetworkErrorMessage);
  }

  if (!response.ok) {
    throw new Error(await getBackendErrorMessage(response, "No fue posible cargar las opciones del formulario."));
  }

  let data: unknown;

  try {
    data = await response.json();
  } catch {
    throw new Error("El backend devolvió una respuesta de catálogos inválida.");
  }

  if (!isBackendEmergencyCatalogs(data)) {
    throw new Error("El backend devolvió una respuesta de catálogos inválida.");
  }

  return mapEmergencyCatalogs(data);
}

export async function createBackendEmergency(payload: CreateBackendEmergencyInput): Promise<BackendEmergency> {
  let response: Response;

  try {
    response = await fetch(buildApiUrl("/api/v1/emergencies/"), {
      body: JSON.stringify(payload),
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
    });
  } catch {
    throw new Error(createEmergencyNetworkErrorMessage);
  }

  if (!response.ok) {
    const fallbackMessage =
      response.status === 400 || response.status === 422
        ? "Revisa los datos del reporte e inténtalo nuevamente."
        : "No fue posible registrar la emergencia.";

    throw new Error(await getBackendErrorMessage(response, fallbackMessage));
  }

  let data: unknown;

  try {
    data = await response.json();
  } catch {
    throw new Error("El backend devolvió una respuesta de emergencia inválida.");
  }

  if (!isBackendEmergency(data)) {
    throw new Error("El backend devolvió una respuesta de emergencia inválida.");
  }

  return data;
}
