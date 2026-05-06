import { useState } from "react";
import { StyleSheet, Text, TextInput, View } from "react-native";

import { AppLayout } from "../components/AppLayout";
import { PrimaryButton } from "../components/PrimaryButton";
import { colors, radii, shadows, spacing } from "../styles/theme";

interface LoginScreenProps {
  onLoginSuccess: () => void;
}

export function isBasicRutFormat(rut: string) {
  const trimmedRut = rut.trim();
  const rutPattern = /^\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]$/;

  return rutPattern.test(trimmedRut);
}

// Login visual inicial. La autenticacion real se conectara al backend en otra iteracion.
export function LoginScreen({ onLoginSuccess }: LoginScreenProps) {
  const [rut, setRut] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = () => {
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
    onLoginSuccess();
  };

  return (
    <AppLayout>
      <View style={styles.container}>
        <View style={styles.brandHeader}>
          <View style={styles.logoMark}>
            <Text style={styles.logoText}>VS</Text>
          </View>
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
              onChangeText={setPassword}
              placeholder="Ingresa tu contraseña"
              placeholderTextColor={colors.textSecondary}
              secureTextEntry
              style={styles.input}
              value={password}
            />
          </View>

          {error ? <Text style={styles.error}>{error}</Text> : null}

          <PrimaryButton label="Ingresar" onPress={handleLogin} />
        </View>
      </View>
    </AppLayout>
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
  logoMark: {
    alignItems: "center",
    backgroundColor: colors.white,
    borderColor: colors.success,
    borderRadius: radii.lg,
    borderWidth: 3,
    height: 76,
    justifyContent: "center",
    width: 76,
    ...shadows.card,
  },
  logoText: {
    color: colors.primary,
    fontSize: 24,
    fontWeight: "900",
  },
  title: {
    color: colors.text,
    fontSize: 22,
    fontWeight: "800",
  },
});
