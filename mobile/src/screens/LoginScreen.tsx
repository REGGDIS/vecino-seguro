import { StyleSheet, Text, TextInput, View } from "react-native";

import { PrimaryButton } from "../components/PrimaryButton";

// Pantalla base de login. El flujo real usará RUT chileno y contraseña segura.
export function LoginScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Ingresar</Text>
      <TextInput placeholder="RUT" style={styles.input} />
      <TextInput placeholder="Contraseña" secureTextEntry style={styles.input} />
      <PrimaryButton label="Iniciar sesión" onPress={() => undefined} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    gap: 12,
    justifyContent: "center",
    padding: 24,
  },
  input: {
    borderColor: "#CBD5E1",
    borderRadius: 8,
    borderWidth: 1,
    padding: 12,
  },
  title: {
    fontSize: 24,
    fontWeight: "700",
  },
});

