import { useEffect, useState } from "react";
import { StyleSheet, Text, View } from "react-native";

import { AppLayout } from "../components/AppLayout";
import { EmergencyCard } from "../components/EmergencyCard";
import { PrimaryButton } from "../components/PrimaryButton";
import { getEmergencies } from "../services/emergencyService";
import { colors, radii, shadows, spacing } from "../styles/theme";
import type { AuthenticatedUser } from "../types/auth";
import type { Emergency } from "../types/emergency";

interface HomeScreenProps {
  onLogout: () => void;
  onRegisterEmergency: () => void;
  onViewEmergencies: () => void;
  user: AuthenticatedUser | null;
}

interface SummaryItem {
  color: string;
  key: string;
  label: string;
  matches: (emergency: Emergency) => boolean;
}

const summaryConfig: SummaryItem[] = [
  {
    color: colors.warning,
    key: "pending",
    label: "Pendientes",
    matches: (emergency) => emergency.status === "pending",
  },
  {
    color: colors.info,
    key: "in_review",
    label: "En revisión",
    matches: (emergency) => emergency.status === "in_review",
  },
  {
    color: colors.success,
    key: "resolved",
    label: "Resueltas",
    matches: (emergency) => emergency.status === "resolved",
  },
  {
    color: colors.danger,
    key: "critical",
    label: "Críticas",
    matches: (emergency) => emergency.urgencyLevel === "critical",
  },
];

const getRoleLabel = (roleId?: number) => (roleId === 1 ? "Administrador" : "Vecino");

export function HomeScreen({ onLogout, onRegisterEmergency, onViewEmergencies, user }: HomeScreenProps) {
  const [emergencies, setEmergencies] = useState<Emergency[]>([]);
  const [errorMessage, setErrorMessage] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const latestEmergencies = emergencies.slice(0, 3);

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

  const renderLatestEmergencies = () => {
    if (isLoading) {
      return <Text style={styles.feedbackText}>Cargando emergencias...</Text>;
    }

    if (errorMessage) {
      return <Text style={styles.errorText}>{errorMessage}</Text>;
    }

    if (latestEmergencies.length === 0) {
      return <Text style={styles.feedbackText}>No hay emergencias registradas.</Text>;
    }

    return latestEmergencies.map((emergency) => <EmergencyCard emergency={emergency} key={emergency.id} />);
  };

  return (
    <AppLayout
      subtitle="Bienvenido al panel comunitario. Revisa reportes recientes y registra nuevas alertas vecinales."
      title="VecinoSeguro"
    >
      <View style={styles.sessionCard}>
        <Text style={styles.sessionGreeting}>Hola, {user?.fullName ?? "vecino"}</Text>
        <Text style={styles.sessionRole}>Sesión iniciada como {getRoleLabel(user?.roleId)}</Text>
      </View>

      <View style={styles.actionRow}>
        <PrimaryButton label="Registrar emergencia" onPress={onRegisterEmergency} />
        <PrimaryButton label="Cerrar sesión" onPress={onLogout} variant="outline" />
      </View>

      <View style={styles.summaryGrid}>
        {summaryConfig.map((item) => {
          const count = emergencies.filter(item.matches).length;

          return (
            <View key={item.key} style={styles.summaryCard}>
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
          <Text style={styles.sectionSubtitle}>Últimos reportes registrados en la comunidad.</Text>
        </View>
      </View>

      <View style={styles.list}>{renderLatestEmergencies()}</View>

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
  sessionCard: {
    backgroundColor: colors.white,
    borderColor: colors.border,
    borderRadius: radii.md,
    borderWidth: 1,
    gap: spacing.xs,
    marginBottom: spacing.lg,
    padding: spacing.lg,
    ...shadows.card,
  },
  sessionGreeting: {
    color: colors.text,
    fontSize: 18,
    fontWeight: "800",
  },
  sessionRole: {
    color: colors.textSecondary,
    fontSize: 14,
    fontWeight: "600",
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
