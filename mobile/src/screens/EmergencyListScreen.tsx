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
  const [errorMessage, setErrorMessage] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;

    async function loadEmergencies() {
      try {
        const items = await getEmergencies();

        if (isMounted) {
          setEmergencies(items);
          setErrorMessage("");
        }
      } catch {
        if (isMounted) {
          setErrorMessage("No fue posible cargar las emergencias. Verifica que el backend esté disponible.");
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadEmergencies();

    return () => {
      isMounted = false;
    };
  }, []);

  const renderEmergencies = () => {
    if (isLoading) {
      return <Text style={styles.feedbackText}>Cargando emergencias...</Text>;
    }

    if (errorMessage) {
      return <Text style={styles.errorText}>{errorMessage}</Text>;
    }

    if (emergencies.length === 0) {
      return <Text style={styles.feedbackText}>No hay emergencias registradas.</Text>;
    }

    return emergencies.map((emergency) => <EmergencyCard emergency={emergency} key={emergency.id} />);
  };

  return (
    <AppLayout
      subtitle="Reportes registrados por la comunidad con sus estados, urgencias y ubicaciones."
      title="Emergencias"
    >
      <View style={styles.actions}>
        <PrimaryButton label="Registrar emergencia" onPress={onRegisterEmergency} />
        <PrimaryButton label="Volver al inicio" onPress={onBack} variant="outline" />
      </View>

      <View style={styles.sectionHeader}>
        <Text style={styles.sectionTitle}>Reportes comunitarios</Text>
        <Text style={styles.sectionSubtitle}>{emergencies.length} reportes disponibles.</Text>
      </View>

      <View style={styles.list}>{renderEmergencies()}</View>
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
  errorText: {
    color: colors.danger,
    fontSize: 14,
    fontWeight: "600",
    lineHeight: 20,
  },
  feedbackText: {
    color: colors.textSecondary,
    fontSize: 14,
    fontWeight: "600",
    lineHeight: 20,
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
