export type EmergencyStatus = "pending" | "in_review" | "resolved" | "critical";

export type UrgencyLevel = "low" | "medium" | "high" | "critical";

export interface CatalogOption {
  value: string;
  label: string;
}

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

export interface BackendEmergencyCatalogs {
  emergency_types: CatalogOption[];
  urgency_levels: CatalogOption[];
  statuses: CatalogOption[];
}

export interface EmergencyCatalogs {
  emergencyTypes: CatalogOption[];
  urgencyLevels: CatalogOption[];
}

export interface CreateBackendEmergencyInput {
  user_id: number;
  type: string;
  description: string;
  location: string;
  urgency_level: string;
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
  userId: number;
  type: string;
  description: string;
  location: string;
  urgencyLevel: string;
}
