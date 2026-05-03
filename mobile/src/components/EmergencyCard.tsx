import { StyleSheet, Text, View } from "react-native";

import { colors, radii, shadows, spacing } from "../styles/theme";
import { StatusBadge } from "./StatusBadge";
import type { Emergency } from "../types/emergency";
import type { UrgencyLevel } from "../types/emergency";

interface EmergencyCardProps {
  emergency: Emergency;
}

const urgencyConfig: Record<UrgencyLevel, { color: string; label: string }> = {
  critical: { color: colors.danger, label: "Crítica" },
  high: { color: colors.warning, label: "Alta" },
  low: { color: colors.success, label: "Baja" },
  medium: { color: colors.info, label: "Media" },
};

function formatDate(value: string) {
  return new Intl.DateTimeFormat("es-CL", {
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    month: "short",
  }).format(new Date(value));
}

// Tarjeta base para mostrar una emergencia en listados o paneles.
export function EmergencyCard({ emergency }: EmergencyCardProps) {
  const urgency = urgencyConfig[emergency.urgencyLevel];

  return (
    <View style={styles.card}>
      <View style={styles.header}>
        <View style={styles.titleGroup}>
          <Text style={styles.title}>{emergency.type}</Text>
          <Text style={styles.location}>{emergency.location}</Text>
        </View>
        <StatusBadge status={emergency.status} />
      </View>

      <Text style={styles.description}>{emergency.description}</Text>

      <View style={styles.metaRow}>
        <View style={styles.urgencyGroup}>
          <View style={[styles.urgencyDot, { backgroundColor: urgency.color }]} />
          <Text style={styles.metaText}>Urgencia {urgency.label}</Text>
        </View>
        <Text style={styles.metaText}>{formatDate(emergency.createdAt)}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.white,
    borderColor: colors.border,
    borderRadius: radii.md,
    borderWidth: 1,
    gap: spacing.md,
    padding: spacing.lg,
    ...shadows.card,
  },
  description: {
    color: colors.text,
    fontSize: 14,
    lineHeight: 20,
  },
  header: {
    alignItems: "flex-start",
    flexDirection: "row",
    gap: spacing.md,
    justifyContent: "space-between",
  },
  location: {
    color: colors.textSecondary,
    fontSize: 13,
    marginTop: spacing.xs,
  },
  metaRow: {
    alignItems: "center",
    borderTopColor: colors.border,
    borderTopWidth: 1,
    flexDirection: "row",
    justifyContent: "space-between",
    paddingTop: spacing.md,
  },
  metaText: {
    color: colors.textSecondary,
    fontSize: 12,
    fontWeight: "600",
  },
  title: {
    color: colors.text,
    fontSize: 17,
    fontWeight: "800",
  },
  titleGroup: {
    flex: 1,
    paddingRight: spacing.sm,
  },
  urgencyDot: {
    borderRadius: radii.pill,
    height: 9,
    width: 9,
  },
  urgencyGroup: {
    alignItems: "center",
    flexDirection: "row",
    gap: spacing.sm,
  },
});
