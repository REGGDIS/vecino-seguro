import { mockEmergencies } from "../data/mockEmergencies";
import { getBackendEmergencies } from "./apiClient";
import type {
  BackendEmergency,
  CreateEmergencyInput,
  Emergency,
  EmergencyStatus,
  UrgencyLevel,
} from "../types/emergency";

let emergencyStore: Emergency[] = [...mockEmergencies];

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

export async function getEmergencies(): Promise<Emergency[]> {
  const backendEmergencies = await getBackendEmergencies();

  return backendEmergencies.map(mapBackendEmergency);
}

export async function getEmergencyById(id: string): Promise<Emergency | null> {
  const emergency = (await getEmergencies()).find((item) => item.id === id);

  return emergency ? cloneEmergency(emergency) : null;
}

export async function createEmergency(input: CreateEmergencyInput): Promise<Emergency> {
  const emergency: Emergency = {
    id: `emg-${Date.now()}`,
    type: input.type.trim(),
    description: input.description.trim(),
    location: input.location.trim(),
    status: "pending",
    urgencyLevel: input.urgencyLevel,
    createdAt: new Date().toISOString(),
  };

  emergencyStore = [emergency, ...emergencyStore];

  return cloneEmergency(emergency);
}
