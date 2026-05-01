import { Pressable, StyleSheet, Text } from "react-native";

interface PrimaryButtonProps {
  label: string;
  onPress: () => void;
}

// Botón reutilizable para acciones principales de la app móvil.
export function PrimaryButton({ label, onPress }: PrimaryButtonProps) {
  return (
    <Pressable accessibilityRole="button" onPress={onPress} style={styles.button}>
      <Text style={styles.label}>{label}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  button: {
    alignItems: "center",
    backgroundColor: "#0F766E",
    borderRadius: 8,
    paddingHorizontal: 16,
    paddingVertical: 12,
  },
  label: {
    color: "#FFFFFF",
    fontWeight: "700",
  },
});

