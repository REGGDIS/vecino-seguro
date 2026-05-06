import { StyleSheet, Text, View } from "react-native";

import { AppLayout } from "../components/AppLayout";
import { EmergencyCard } from "../components/EmergencyCard";
import { PrimaryButton } from "../components/PrimaryButton";
import { mockEmergencies } from "../data/mockEmergencies";
import { colors, spacing } from "../styles/theme";

interface EmergencyListScreenProps {
  onBack: () => void;
  onRegisterEmergency: () => void;
}

export function EmergencyListScreen({ onBack, onRegisterEmergency }: EmergencyListScreenProps) {
  return (
    <AppLayout
      subtitle="Listado inicial con datos simulados para presentar estados, urgencias y ubicaciones."
      title="Emergencias"
    >
      <View style={styles.actions}>
        <PrimaryButton label="Registrar emergencia" onPress={onRegisterEmergency} />
        <PrimaryButton label="Volver al inicio" onPress={onBack} variant="outline" />
      </View>

      <View style={styles.sectionHeader}>
        <Text style={styles.sectionTitle}>Reportes comunitarios</Text>
        <Text style={styles.sectionSubtitle}>{mockEmergencies.length} reportes simulados disponibles.</Text>
      </View>

      <View style={styles.list}>
        {mockEmergencies.map((emergency) => (
          <EmergencyCard emergency={emergency} key={emergency.id} />
        ))}
      </View>
    </AppLayout>
  );
}

const styles = StyleSheet.create({
  actions: {
    gap: spacing.md,
    marginBottom: spacing.xl,
  },
  list: {
    gap: spacing.md,
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
});
