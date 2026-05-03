import type { Emergency } from "../types/emergency";

export const mockEmergencies: Emergency[] = [
  {
    id: "emg-001",
    type: "Alumbrado público apagado",
    description: "Poste sin luz durante la noche, aumenta la sensación de inseguridad en la cuadra.",
    location: "Calle Los Álamos 123",
    status: "resolved",
    urgencyLevel: "medium",
    createdAt: "2026-05-01T20:15:00.000Z",
  },
  {
    id: "emg-002",
    type: "Accidente de tránsito",
    description: "Colisión menor con obstrucción parcial de la vía principal.",
    location: "Av. Central con 5 de Mayo",
    status: "critical",
    urgencyLevel: "critical",
    createdAt: "2026-05-03T08:40:00.000Z",
  },
  {
    id: "emg-003",
    type: "Emergencia médica",
    description: "Vecina solicita apoyo para contactar asistencia médica.",
    location: "Pasaje Las Flores",
    status: "in_review",
    urgencyLevel: "high",
    createdAt: "2026-05-02T16:25:00.000Z",
  },
  {
    id: "emg-004",
    type: "Sospecha de robo",
    description: "Movimiento sospechoso reportado cerca del acceso norte de la plaza.",
    location: "Sector Plaza Norte",
    status: "pending",
    urgencyLevel: "high",
    createdAt: "2026-05-03T11:05:00.000Z",
  },
];
