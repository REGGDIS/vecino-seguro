import { useEffect, useState } from "react";
import { Pressable, StyleSheet, Text, TextInput, View } from "react-native";

import { AppLayout } from "../components/AppLayout";
import { PrimaryButton } from "../components/PrimaryButton";
import { createEmergency, getEmergencyCatalogs } from "../services/emergencyService";
import { colors, radii, shadows, spacing } from "../styles/theme";
import type { AuthenticatedUser } from "../types/auth";
import type { CatalogOption } from "../types/emergency";

interface EmergencyFormScreenProps {
  onBack: () => void;
  user: AuthenticatedUser | null;
}

export function EmergencyFormScreen({ onBack, user }: EmergencyFormScreenProps) {
  const [emergencyTypes, setEmergencyTypes] = useState<CatalogOption[]>([]);
  const [urgencyOptions, setUrgencyOptions] = useState<CatalogOption[]>([]);
  const [type, setType] = useState("");
  const [description, setDescription] = useState("");
  const [location, setLocation] = useState("");
  const [urgencyLevel, setUrgencyLevel] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [catalogError, setCatalogError] = useState("");
  const [isLoadingCatalogs, setIsLoadingCatalogs] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    let isMounted = true;

    async function loadCatalogs() {
      try {
        const catalogs = await getEmergencyCatalogs();

        if (isMounted) {
          setEmergencyTypes(catalogs.emergencyTypes);
          setUrgencyOptions(catalogs.urgencyLevels);
          setCatalogError("");
        }
      } catch {
        if (isMounted) {
          setCatalogError(
            "No fue posible cargar las opciones del formulario. Verifica que el backend esté disponible.",
          );
        }
      } finally {
        if (isMounted) {
          setIsLoadingCatalogs(false);
        }
      }
    }

    loadCatalogs();

    return () => {
      isMounted = false;
    };
  }, []);

  const handleSubmit = async () => {
    const trimmedDescription = description.trim();
    const trimmedLocation = location.trim();

    if (!user) {
      setMessage("");
      setError("No se encontró el usuario autenticado. Vuelve a iniciar sesión.");
      return;
    }

    if (!type) {
      setMessage("");
      setError("Selecciona un tipo de emergencia.");
      return;
    }

    if (!trimmedDescription) {
      setMessage("");
      setError("Describe brevemente lo ocurrido.");
      return;
    }

    if (trimmedDescription.length < 10) {
      setMessage("");
      setError("La descripción debe tener al menos 10 caracteres.");
      return;
    }

    if (!trimmedLocation) {
      setMessage("");
      setError("Indica la ubicación o sector.");
      return;
    }

    if (!urgencyLevel) {
      setMessage("");
      setError("Selecciona un nivel de urgencia.");
      return;
    }

    try {
      setIsSubmitting(true);
      await createEmergency({
        userId: user.id,
        type,
        description: trimmedDescription,
        location: trimmedLocation,
        urgencyLevel,
      });

      setError("");
      setMessage("Emergencia registrada correctamente.");
      setType("");
      setDescription("");
      setLocation("");
      setUrgencyLevel("");
    } catch (submissionError) {
      setMessage("");
      setError(
        submissionError instanceof Error
          ? submissionError.message
          : "No fue posible registrar la emergencia. Inténtalo nuevamente.",
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <AppLayout
      subtitle="Completa los datos principales para registrar un reporte real en la comunidad."
      title="Registrar emergencia"
    >
      <View style={styles.card}>
        <View style={styles.field}>
          <Text style={styles.label}>Tipo de emergencia</Text>
          {isLoadingCatalogs ? <Text style={styles.helperText}>Cargando opciones...</Text> : null}
          {catalogError ? <Text style={styles.error}>{catalogError}</Text> : null}
          {!isLoadingCatalogs && !catalogError ? (
            <View style={styles.optionGrid}>
              {emergencyTypes.map((option) => {
                const selected = type === option.value;

                return (
                  <Pressable
                    accessibilityRole="button"
                    disabled={isSubmitting}
                    key={option.value}
                    onPress={() => setType(option.value)}
                    style={[styles.option, selected && styles.optionSelected]}
                  >
                    <Text style={[styles.optionLabel, selected && styles.optionLabelSelected]}>{option.label}</Text>
                  </Pressable>
                );
              })}
            </View>
          ) : null}
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
          <View style={styles.optionGrid}>
            {urgencyOptions.map((option) => {
              const selected = urgencyLevel === option.value;

              return (
                <Pressable
                  accessibilityRole="button"
                  disabled={isSubmitting || isLoadingCatalogs || !!catalogError}
                  key={option.value}
                  onPress={() => setUrgencyLevel(option.value)}
                  style={[styles.option, selected && styles.optionSelected]}
                >
                  <Text style={[styles.optionLabel, selected && styles.optionLabelSelected]}>{option.label}</Text>
                </Pressable>
              );
            })}
          </View>
        </View>

        {error ? <Text style={styles.error}>{error}</Text> : null}
        {!user && !error ? (
          <Text style={styles.error}>No se encontró el usuario autenticado. Vuelve a iniciar sesión.</Text>
        ) : null}
        {message ? <Text style={styles.success}>{message}</Text> : null}

        <PrimaryButton
          disabled={!user || isSubmitting || isLoadingCatalogs || !!catalogError}
          label={isSubmitting ? "Registrando..." : "Registrar emergencia"}
          onPress={handleSubmit}
        />
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
  helperText: {
    color: colors.textSecondary,
    fontSize: 14,
    fontWeight: "600",
  },
  option: {
    alignItems: "center",
    borderColor: colors.border,
    borderRadius: radii.pill,
    borderWidth: 1,
    justifyContent: "center",
    minHeight: 40,
    paddingHorizontal: spacing.lg,
  },
  optionGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: spacing.sm,
  },
  optionLabel: {
    color: colors.textSecondary,
    fontSize: 14,
    fontWeight: "700",
  },
  optionLabelSelected: {
    color: colors.white,
  },
  optionSelected: {
    backgroundColor: colors.primary,
    borderColor: colors.primary,
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
});
