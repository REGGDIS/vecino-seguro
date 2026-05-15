export type EmergencyStatus = "pending" | "in_review" | "resolved" | "critical";

export type UrgencyLevel = "low" | "medium" | "high" | "critical";

export interface BackendEmergency {
  id: number;
  user_id: number;
  type: string;
  description: string;
  location: string;
  urgency_level: string;
  status: string;
  created_at: string;
  updated_at: string | null;
}

// Tipo compartido para representar emergencias dentro de la app movil.
export interface Emergency {
  id: string;
  type: string;
  description: string;
  location: string;
  status: EmergencyStatus;
  urgencyLevel: UrgencyLevel;
  createdAt: string;
}

export interface CreateEmergencyInput {
  type: string;
  description: string;
  location: string;
  urgencyLevel: UrgencyLevel;
}
