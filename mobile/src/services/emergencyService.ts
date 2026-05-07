import { mockEmergencies } from "../data/mockEmergencies";
import type { CreateEmergencyInput, Emergency } from "../types/emergency";

let emergencyStore: Emergency[] = [...mockEmergencies];

const cloneEmergency = (emergency: Emergency): Emergency => ({ ...emergency });

// Fuente temporal basada en mocks; preparada para reemplazarse por llamadas HTTP.
export async function getEmergencies(): Promise<Emergency[]> {
  return emergencyStore.map(cloneEmergency);
}

export async function getEmergencyById(id: string): Promise<Emergency | null> {
  const emergency = emergencyStore.find((item) => item.id === id);

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
