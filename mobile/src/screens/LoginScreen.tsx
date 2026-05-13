import { useState } from "react";
import { Image, KeyboardAvoidingView, Platform, ScrollView, StyleSheet, Text, TextInput, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

import { PrimaryButton } from "../components/PrimaryButton";
import { login } from "../services/apiClient";
import { colors, radii, shadows, spacing } from "../styles/theme";
import type { AuthenticatedUser } from "../types/auth";

interface LoginScreenProps {
  onLoginSuccess: (user: AuthenticatedUser) => void;
}

export function isBasicRutFormat(rut: string) {
  const trimmedRut = rut.trim();
  const rutPattern = /^\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]$/;

  return rutPattern.test(trimmedRut);
}

export function LoginScreen({ onLoginSuccess }: LoginScreenProps) {
  const [rut, setRut] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleLogin = async () => {
    if (isSubmitting) {
      return;
    }

    if (!rut.trim()) {
      setError("Ingresa tu RUT para continuar.");
      return;
    }

    if (!isBasicRutFormat(rut)) {
      setError("Usa un formato de RUT válido, por ejemplo 12.345.678-9.");
      return;
    }

    if (!password.trim()) {
      setError("Ingresa tu contraseña para continuar.");
      return;
    }

    setError("");
    setIsSubmitting(true);

    try {
      const response = await login(rut, password);
      onLoginSuccess(response.user);
    } catch (loginError) {
      setError(
        loginError instanceof Error
          ? loginError.message
          : "No fue posible iniciar sesión. Inténtalo nuevamente.",
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <KeyboardAvoidingView
        behavior={Platform.OS === "ios" ? "padding" : "height"}
        style={styles.keyboardAvoidingView}
      >
        <ScrollView
          contentContainerStyle={styles.scrollContent}
          keyboardShouldPersistTaps="handled"
          showsVerticalScrollIndicator={false}
        >
          <View style={styles.container}>
            <View style={styles.brandHeader}>
              <Image
                accessibilityLabel="Isotipo VecinoSeguro"
                resizeMode="contain"
                source={require("../assets/isotipo-vecino-seguro.png")}
                style={styles.logo}
              />
              <Text style={styles.brandName}>
                Vecino<Text style={styles.brandAccent}>Seguro</Text>
              </Text>
              <Text style={styles.description}>
                Reporta emergencias y coordina ayuda vecinal de forma rápida y segura.
              </Text>
            </View>

            <View style={styles.card}>
              <Text style={styles.title}>Ingreso vecinal</Text>
              <Text style={styles.helper}>Usa tus credenciales comunitarias para acceder al panel móvil.</Text>

              <View style={styles.field}>
                <Text style={styles.label}>RUT</Text>
                <TextInput
                  accessibilityLabel="RUT"
                  autoCapitalize="characters"
                  keyboardType="default"
                  onChangeText={setRut}
                  placeholder="12.345.678-9"
                  placeholderTextColor={colors.textSecondary}
                  style={styles.input}
                  value={rut}
                />
              </View>

              <View style={styles.field}>
                <Text style={styles.label}>Contraseña</Text>
                <TextInput
                  accessibilityLabel="Contraseña"
                  onChangeText={setPassword}
                  placeholder="Ingresa tu contraseña"
                  placeholderTextColor={colors.textSecondary}
                  onSubmitEditing={() => {
                    void handleLogin();
                  }}
                  returnKeyType="done"
                  secureTextEntry
                  style={styles.input}
                  value={password}
                />
              </View>

              {error ? <Text style={styles.error}>{error}</Text> : null}

              <PrimaryButton
                disabled={isSubmitting}
                label={isSubmitting ? "Ingresando..." : "Ingresar"}
                onPress={() => {
                  void handleLogin();
                }}
              />
            </View>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  brandAccent: {
    color: colors.success,
  },
  brandHeader: {
    alignItems: "center",
    gap: spacing.sm,
    marginBottom: spacing.xl,
  },
  brandName: {
    color: colors.darkBlue,
    fontSize: 32,
    fontWeight: "800",
  },
  card: {
    backgroundColor: colors.white,
    borderColor: colors.border,
    borderRadius: radii.lg,
    borderWidth: 1,
    gap: spacing.lg,
    padding: spacing.xl,
    ...shadows.card,
  },
  container: {
    flex: 1,
    justifyContent: "center",
    width: "100%",
  },
  description: {
    color: colors.textSecondary,
    fontSize: 15,
    lineHeight: 21,
    maxWidth: 300,
    textAlign: "center",
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
  helper: {
    color: colors.textSecondary,
    fontSize: 14,
    lineHeight: 20,
  },
  input: {
    backgroundColor: colors.white,
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
  keyboardAvoidingView: {
    flex: 1,
  },
  logo: {
    alignSelf: "center",
    height: 116,
    marginBottom: spacing.sm,
    width: 116,
    ...shadows.card,
  },
  safeArea: {
    backgroundColor: colors.surface,
    flex: 1,
  },
  scrollContent: {
    flexGrow: 1,
    justifyContent: "center",
    padding: spacing.xl,
    paddingBottom: spacing.xxl,
  },
  title: {
    color: colors.text,
    fontSize: 22,
    fontWeight: "800",
  },
});
