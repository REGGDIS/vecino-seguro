import {
  createBackendEmergency,
  getBackendEmergencies,
  getEmergencyCatalogs as fetchEmergencyCatalogs,
} from "./apiClient";
import type {
  BackendEmergency,
  CreateEmergencyInput,
  Emergency,
  EmergencyCatalogs,
  EmergencyStatus,
  UrgencyLevel,
} from "../types/emergency";

const cloneEmergency = (emergency: Emergency): Emergency => ({ ...emergency });

const statusMap: Record<string, EmergencyStatus> = {
  en_revision: "in_review",
  pendiente: "pending",
  resuelto: "resolved",
};

const urgencyMap: Record<string, UrgencyLevel> = {
  alta: "high",
  baja: "low",
  critica: "critical",
  crítica: "critical",
  media: "medium",
};

const typeLabels: Record<string, string> = {
  accidente: "Accidente",
  corte_luz: "Corte de luz",
  emergencia_medica: "Emergencia médica",
  incendio: "Incendio",
  otro: "Otro",
  persona_extraviada: "Persona extraviada",
  robo: "Robo",
  solicitud_ayuda: "Solicitud de ayuda",
};

function normalizeBackendValue(value: string) {
  return value.trim().toLowerCase();
}

function toReadableType(value: string) {
  const normalizedValue = normalizeBackendValue(value);
  const mappedLabel = typeLabels[normalizedValue];

  if (mappedLabel) {
    return mappedLabel;
  }

  const readableValue = normalizedValue.replace(/_/g, " ");

  return readableValue.charAt(0).toUpperCase() + readableValue.slice(1);
}

function mapBackendEmergency(emergency: BackendEmergency): Emergency {
  return {
    createdAt: emergency.created_at,
    description: emergency.description,
    id: String(emergency.id),
    location: emergency.location,
    status: statusMap[normalizeBackendValue(emergency.status)] ?? "pending",
    type: toReadableType(emergency.type),
    urgencyLevel: urgencyMap[normalizeBackendValue(emergency.urgency_level)] ?? "medium",
  };
}

export async function getEmergencyCatalogs(): Promise<EmergencyCatalogs> {
  return fetchEmergencyCatalogs();
}

export async function getEmergencies(): Promise<Emergency[]> {
  const backendEmergencies = await getBackendEmergencies();

  return backendEmergencies.map(mapBackendEmergency);
}

export async function getEmergencyById(id: string): Promise<Emergency | null> {
  const emergency = (await getEmergencies()).find((item) => item.id === id);

  return emergency ? cloneEmergency(emergency) : null;
}

export async function createEmergency(input: CreateEmergencyInput): Promise<Emergency> {
  const backendEmergency = await createBackendEmergency({
    description: input.description.trim(),
    location: input.location.trim(),
    type: input.type.trim(),
    urgency_level: input.urgencyLevel.trim(),
    user_id: input.userId,
  });

  return mapBackendEmergency(backendEmergency);
}
