import { StyleSheet, Text, View } from "react-native";

import { AppLayout } from "../components/AppLayout";
import { EmergencyCard } from "../components/EmergencyCard";
import { PrimaryButton } from "../components/PrimaryButton";
import { mockEmergencies } from "../data/mockEmergencies";
import { colors, radii, shadows, spacing } from "../styles/theme";
import type { EmergencyStatus } from "../types/emergency";

interface HomeScreenProps {
  onLogout: () => void;
  onRegisterEmergency: () => void;
  onViewEmergencies: () => void;
}

const summaryConfig: Array<{ label: string; status: EmergencyStatus; color: string }> = [
  { color: colors.warning, label: "Pendientes", status: "pending" },
  { color: colors.info, label: "En revisión", status: "in_review" },
  { color: colors.success, label: "Resueltas", status: "resolved" },
  { color: colors.danger, label: "Críticas", status: "critical" },
];

export function HomeScreen({ onLogout, onRegisterEmergency, onViewEmergencies }: HomeScreenProps) {
  const latestEmergencies = mockEmergencies.slice(0, 3);

  return (
    <AppLayout
      subtitle="Bienvenido al panel comunitario. Revisa reportes recientes y registra nuevas alertas vecinales."
      title="VecinoSeguro"
    >
      <View style={styles.actionRow}>
        <PrimaryButton label="Registrar emergencia" onPress={onRegisterEmergency} />
        <PrimaryButton label="Cerrar sesión" onPress={onLogout} variant="outline" />
      </View>

      <View style={styles.summaryGrid}>
        {summaryConfig.map((item) => {
          const count = mockEmergencies.filter((emergency) => emergency.status === item.status).length;

          return (
            <View key={item.status} style={styles.summaryCard}>
              <View style={[styles.summaryIndicator, { backgroundColor: item.color }]} />
              <Text style={styles.summaryCount}>{count}</Text>
              <Text style={styles.summaryLabel}>{item.label}</Text>
            </View>
          );
        })}
      </View>

      <View style={styles.sectionHeader}>
        <View>
          <Text style={styles.sectionTitle}>Últimos reportes</Text>
          <Text style={styles.sectionSubtitle}>Emergencias simuladas para validar el flujo inicial.</Text>
        </View>
      </View>

      <View style={styles.list}>
        {latestEmergencies.map((emergency) => (
          <EmergencyCard emergency={emergency} key={emergency.id} />
        ))}
      </View>

      <PrimaryButton label="Ver listado completo" onPress={onViewEmergencies} variant="secondary" />
    </AppLayout>
  );
}

const styles = StyleSheet.create({
  actionRow: {
    gap: spacing.md,
    marginBottom: spacing.xl,
  },
  list: {
    gap: spacing.md,
    marginBottom: spacing.lg,
  },
  sectionHeader: {
    marginBottom: spacing.md,
  },
  sectionSubtitle: {
    color: colors.textSecondary,
    fontSize: 14,
    marginTop: spacing.xs,
  },
  sectionTitle: {
    color: colors.text,
    fontSize: 20,
    fontWeight: "800",
  },
  summaryCard: {
    backgroundColor: colors.white,
    borderColor: colors.border,
    borderRadius: radii.md,
    borderWidth: 1,
    flexBasis: "47%",
    gap: spacing.xs,
    overflow: "hidden",
    padding: spacing.lg,
    ...shadows.card,
  },
  summaryCount: {
    color: colors.darkBlue,
    fontSize: 26,
    fontWeight: "900",
  },
  summaryGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: spacing.md,
    marginBottom: spacing.xl,
  },
  summaryIndicator: {
    borderRadius: radii.pill,
    height: 5,
    marginBottom: spacing.sm,
    width: 44,
  },
  summaryLabel: {
    color: colors.textSecondary,
    fontSize: 13,
    fontWeight: "700",
  },
});
