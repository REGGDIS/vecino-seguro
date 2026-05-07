import { useEffect, useState } from "react";
import { StyleSheet, Text, View } from "react-native";

import { AppLayout } from "../components/AppLayout";
import { EmergencyCard } from "../components/EmergencyCard";
import { PrimaryButton } from "../components/PrimaryButton";
import { getEmergencies } from "../services/emergencyService";
import { colors, spacing } from "../styles/theme";
import type { Emergency } from "../types/emergency";

interface EmergencyListScreenProps {
  onBack: () => void;
  onRegisterEmergency: () => void;
}

export function EmergencyListScreen({ onBack, onRegisterEmergency }: EmergencyListScreenProps) {
  const [emergencies, setEmergencies] = useState<Emergency[]>([]);

  useEffect(() => {
    let isMounted = true;

    getEmergencies().then((items) => {
      if (isMounted) {
        setEmergencies(items);
      }
    });

    return () => {
      isMounted = false;
    };
  }, []);

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
        <Text style={styles.sectionSubtitle}>{emergencies.length} reportes simulados disponibles.</Text>
      </View>

      <View style={styles.list}>
        {emergencies.map((emergency) => (
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
