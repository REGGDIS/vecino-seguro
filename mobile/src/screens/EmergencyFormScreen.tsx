import { useState } from "react";
import { Pressable, StyleSheet, Text, TextInput, View } from "react-native";

import { AppLayout } from "../components/AppLayout";
import { PrimaryButton } from "../components/PrimaryButton";
import { colors, radii, shadows, spacing } from "../styles/theme";
import type { UrgencyLevel } from "../types/emergency";

interface EmergencyFormScreenProps {
  onBack: () => void;
}

const urgencyOptions: Array<{ label: string; value: UrgencyLevel }> = [
  { label: "Baja", value: "low" },
  { label: "Media", value: "medium" },
  { label: "Alta", value: "high" },
  { label: "Crítica", value: "critical" },
];

// Registro visual simulado; no guarda en backend real en esta etapa.
export function EmergencyFormScreen({ onBack }: EmergencyFormScreenProps) {
  const [type, setType] = useState("");
  const [description, setDescription] = useState("");
  const [location, setLocation] = useState("");
  const [urgencyLevel, setUrgencyLevel] = useState<UrgencyLevel>("medium");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = () => {
    if (!type.trim() || !description.trim() || !location.trim()) {
      setMessage("");
      setError("Completa tipo, descripción y ubicación para registrar el reporte.");
      return;
    }

    setError("");
    setMessage("Emergencia registrada de forma simulada. La conexión real quedará para una futura iteración.");
    setType("");
    setDescription("");
    setLocation("");
    setUrgencyLevel("medium");
  };

  return (
    <AppLayout
      subtitle="Completa los datos principales para dejar preparado el flujo de reporte móvil."
      title="Registrar emergencia"
    >
      <View style={styles.card}>
        <View style={styles.field}>
          <Text style={styles.label}>Tipo de emergencia</Text>
          <TextInput
            onChangeText={setType}
            placeholder="Ej: Accidente, robo, emergencia medica"
            placeholderTextColor={colors.textSecondary}
            style={styles.input}
            value={type}
          />
        </View>

        <View style={styles.field}>
            <Text style={styles.label}>Descripción</Text>
          <TextInput
            multiline
            onChangeText={setDescription}
            placeholder="Describe brevemente lo ocurrido"
            placeholderTextColor={colors.textSecondary}
            style={[styles.input, styles.textArea]}
            value={description}
          />
        </View>

        <View style={styles.field}>
          <Text style={styles.label}>Ubicación o sector</Text>
          <TextInput
            onChangeText={setLocation}
            placeholder="Ej: Pasaje Las Flores"
            placeholderTextColor={colors.textSecondary}
            style={styles.input}
            value={location}
          />
        </View>

        <View style={styles.field}>
          <Text style={styles.label}>Nivel de urgencia</Text>
          <View style={styles.urgencyGrid}>
            {urgencyOptions.map((option) => {
              const selected = urgencyLevel === option.value;

              return (
                <Pressable
                  accessibilityRole="button"
                  key={option.value}
                  onPress={() => setUrgencyLevel(option.value)}
                  style={[styles.urgencyOption, selected && styles.urgencyOptionSelected]}
                >
                  <Text style={[styles.urgencyLabel, selected && styles.urgencyLabelSelected]}>{option.label}</Text>
                </Pressable>
              );
            })}
          </View>
        </View>

        {error ? <Text style={styles.error}>{error}</Text> : null}
        {message ? <Text style={styles.success}>{message}</Text> : null}

        <PrimaryButton label="Registrar emergencia" onPress={handleSubmit} />
        <PrimaryButton label="Volver al inicio" onPress={onBack} variant="outline" />
      </View>
    </AppLayout>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.white,
    borderColor: colors.border,
    borderRadius: radii.lg,
    borderWidth: 1,
    gap: spacing.lg,
    padding: spacing.xl,
    ...shadows.card,
  },
  error: {
    backgroundColor: "#FDECEC",
    borderRadius: radii.sm,
    color: colors.danger,
    fontSize: 14,
    fontWeight: "600",
    padding: spacing.md,
  },
  field: {
    gap: spacing.sm,
  },
  input: {
    borderColor: colors.border,
    borderRadius: radii.md,
    borderWidth: 1,
    color: colors.text,
    fontSize: 16,
    minHeight: 48,
    paddingHorizontal: spacing.md,
  },
  label: {
    color: colors.text,
    fontSize: 14,
    fontWeight: "700",
  },
  success: {
    backgroundColor: "#E7F8EA",
    borderRadius: radii.sm,
    color: colors.darkGreen,
    fontSize: 14,
    fontWeight: "600",
    padding: spacing.md,
  },
  textArea: {
    minHeight: 112,
    paddingTop: spacing.md,
    textAlignVertical: "top",
  },
  urgencyGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: spacing.sm,
  },
  urgencyLabel: {
    color: colors.textSecondary,
    fontSize: 14,
    fontWeight: "700",
  },
  urgencyLabelSelected: {
    color: colors.white,
  },
  urgencyOption: {
    alignItems: "center",
    borderColor: colors.border,
    borderRadius: radii.pill,
    borderWidth: 1,
    minHeight: 40,
    justifyContent: "center",
    paddingHorizontal: spacing.lg,
  },
  urgencyOptionSelected: {
    backgroundColor: colors.primary,
    borderColor: colors.primary,
  },
});
