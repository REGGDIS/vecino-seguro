import { Pressable, StyleSheet, Text } from "react-native";

import { colors, radii, spacing } from "../styles/theme";

type PrimaryButtonVariant = "primary" | "secondary" | "outline";

interface PrimaryButtonProps {
  disabled?: boolean;
  label: string;
  onPress: () => void;
  variant?: PrimaryButtonVariant;
}

// Boton reutilizable para acciones principales y secundarias de la app movil.
export function PrimaryButton({ disabled = false, label, onPress, variant = "primary" }: PrimaryButtonProps) {
  return (
    <Pressable
      accessibilityRole="button"
      disabled={disabled}
      onPress={onPress}
      style={({ pressed }) => [
        styles.button,
        styles[variant],
        disabled && styles.disabled,
        pressed && !disabled && styles.pressed,
      ]}
    >
      <Text style={[styles.label, variant === "outline" && styles.outlineLabel]}>{label}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  button: {
    alignItems: "center",
    borderRadius: radii.md,
    borderWidth: 1,
    minHeight: 48,
    justifyContent: "center",
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.md,
  },
  disabled: {
    opacity: 0.55,
  },
  label: {
    color: colors.white,
    fontSize: 16,
    fontWeight: "700",
  },
  outline: {
    backgroundColor: colors.white,
    borderColor: colors.primary,
  },
  outlineLabel: {
    color: colors.primary,
  },
  pressed: {
    opacity: 0.86,
  },
  primary: {
    backgroundColor: colors.primary,
    borderColor: colors.primary,
  },
  secondary: {
    backgroundColor: colors.success,
    borderColor: colors.success,
  },
});
