import { StyleSheet, Text, View } from "react-native";

import { colors, radii, spacing } from "../styles/theme";
import type { EmergencyStatus } from "../types/emergency";

interface StatusBadgeProps {
  status: EmergencyStatus;
}

const statusConfig: Record<EmergencyStatus, { backgroundColor: string; label: string; textColor: string }> = {
  critical: {
    backgroundColor: "#FDECEC",
    label: "Crítico",
    textColor: colors.danger,
  },
  in_review: {
    backgroundColor: "#EAF3FF",
    label: "En revisión",
    textColor: colors.info,
  },
  pending: {
    backgroundColor: "#FFF6D8",
    label: "Pendiente",
    textColor: "#8A6100",
  },
  resolved: {
    backgroundColor: "#E7F8EA",
    label: "Resuelto",
    textColor: colors.darkGreen,
  },
};

export function StatusBadge({ status }: StatusBadgeProps) {
  const config = statusConfig[status];

  return (
    <View style={[styles.badge, { backgroundColor: config.backgroundColor }]}>
      <Text style={[styles.label, { color: config.textColor }]}>{config.label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  badge: {
    alignSelf: "flex-start",
    borderRadius: radii.pill,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.xs,
  },
  label: {
    fontSize: 12,
    fontWeight: "700",
  },
});
