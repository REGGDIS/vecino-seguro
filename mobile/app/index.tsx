import { StyleSheet, Text, View } from "react-native";

// Punto inicial de la app móvil. Luego se conectará a navegación y pantallas reales.
export default function Index() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>VecinoSeguro</Text>
      <Text style={styles.subtitle}>Aplicación comunitaria de emergencias locales</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: "center",
    flex: 1,
    justifyContent: "center",
    padding: 24,
  },
  subtitle: {
    fontSize: 16,
    marginTop: 8,
    textAlign: "center",
  },
  title: {
    fontSize: 28,
    fontWeight: "700",
  },
});

