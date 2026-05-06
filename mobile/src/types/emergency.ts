export type EmergencyStatus = "pending" | "in_review" | "resolved" | "critical";

export type UrgencyLevel = "low" | "medium" | "high" | "critical";

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
