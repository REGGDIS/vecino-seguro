import { StyleSheet, Text, TextInput, View } from "react-native";

import { PrimaryButton } from "../components/PrimaryButton";

// Pantalla base para registrar una emergencia desde el dispositivo móvil.
export function EmergencyFormScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Registrar emergencia</Text>
      <TextInput placeholder="Tipo" style={styles.input} />
      <TextInput placeholder="Descripción" multiline style={[styles.input, styles.textArea]} />
      <TextInput placeholder="Ubicación" style={styles.input} />
      <TextInput placeholder="Nivel de urgencia" style={styles.input} />
      <PrimaryButton label="Enviar reporte" onPress={() => undefined} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    gap: 12,
    padding: 24,
  },
  input: {
    borderColor: "#CBD5E1",
    borderRadius: 8,
    borderWidth: 1,
    padding: 12,
  },
  textArea: {
    minHeight: 96,
    textAlignVertical: "top",
  },
  title: {
    fontSize: 24,
    fontWeight: "700",
  },
});

