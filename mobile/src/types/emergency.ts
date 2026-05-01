// Tipo compartido para representar emergencias dentro de la app móvil.
export interface Emergency {
  id: number;
  type: string;
  description: string;
  location: string;
  status: string;
  urgencyLevel: "baja" | "media" | "alta" | "crítica";
  createdAt: string;
}

