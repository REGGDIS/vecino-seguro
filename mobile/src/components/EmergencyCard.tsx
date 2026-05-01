import { StyleSheet, Text, View } from "react-native";

import type { Emergency } from "../types/emergency";

interface EmergencyCardProps {
  emergency: Emergency;
}

// Tarjeta base para mostrar una emergencia en listados o paneles.
export function EmergencyCard({ emergency }: EmergencyCardProps) {
  return (
    <View style={styles.card}>
      <Text style={styles.title}>{emergency.type}</Text>
      <Text>{emergency.description}</Text>
      <Text>{emergency.location}</Text>
      <Text>{emergency.status}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    borderColor: "#CBD5E1",
    borderRadius: 8,
    borderWidth: 1,
    gap: 4,
    padding: 12,
  },
  title: {
    fontSize: 18,
    fontWeight: "700",
  },
});

